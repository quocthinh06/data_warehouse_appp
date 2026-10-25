import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from data import REQUIRED, detail_sql, scope, client
from metrics import read_metrics, split_items

ROOT = Path(__file__).resolve().parents[1]
FIELDS = REQUIRED | {"prediction_date"}
ROW = {"patient_nbr": "100", "encounter_id": "200", "risk_score": 0.8,
       "risk_level": "Cao", "top_factors": "number_inpatient | number_emergency",
       "recommended_actions": "Hành động thử A | Hành động thử B"}

class DashboardTests(unittest.TestCase):
    def test_scope(self):
        self.assertIn("MAX(prediction_date)", scope(FIELDS, True))
        self.assertEqual(scope(REQUIRED, True), "TRUE")
        self.assertEqual(scope(FIELDS, False), "TRUE")

    def test_parameterized_filters(self):
        sql, params = detail_sql(FIELDS, True, ["Cao"], 0.5, "123' OR TRUE", 2)
        self.assertNotIn("123' OR TRUE", sql)
        self.assertIn("@patient", sql)
        self.assertIn("LIMIT 101", sql)
        values = {p.name: p for p in params}
        self.assertEqual(values["offset"].value, 100)
        self.assertEqual(values["patient"].value, "123' OR TRUE")

    def test_csv_and_items(self):
        self.assertEqual(read_metrics(io.StringIO("model,auc\nexample,0.7\n")).iloc[0].auc, 0.7)
        self.assertEqual(read_metrics(io.StringIO("metric,value\nrecall,0.6\n")).shape, (1, 2))
        with self.assertRaises(ValueError):
            read_metrics(io.StringIO("model,auc\n"))
        self.assertEqual(split_items(None), ["Chưa có dữ liệu"])
        self.assertEqual(split_items(" A | | B "), ["A", "B"])

    def test_overview(self):
        summary = pd.DataFrame([dict(total_predictions=1, unique_patients=1, avg_score=0.8, min_score=0.8, max_score=0.8)])
        distribution = pd.DataFrame([dict(risk_level="Cao", prediction_count=1, unique_patients=1, avg_score=0.8, min_score=0.8, max_score=0.8)])
        with patch("data.connect", return_value=(None, FIELDS, "US")), patch("data.query", side_effect=[summary, distribution, pd.DataFrame([{"latest": "2026-10-25"}])]):
            app = AppTest.from_file(str(ROOT / "pages/overview.py")).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.metric), 3)

    def test_patient_pages(self):
        for page in ["priority", "explanation"]:
            for rows in [pd.DataFrame([ROW]), pd.DataFrame(columns=ROW)]:
                with self.subTest(page=page, empty=rows.empty), patch("data.connect", return_value=(None, FIELDS, "US")), patch("data.query", return_value=rows):
                    app = AppTest.from_file(str(ROOT / f"pages/{page}.py")).run()
                    self.assertEqual(list(app.exception), [])
                    if rows.empty:
                        self.assertTrue(app.info)

    def test_missing_csv(self):
        exists = Path.exists
        with patch("pathlib.Path.exists", autospec=True, side_effect=lambda path:
                   False if path == ROOT / "data/evaluation_metrics.csv" else exists(path)):
            app = AppTest.from_file(str(ROOT / "pages/performance.py")).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(app.info)

    def test_provided_metrics(self):
        frame = read_metrics(ROOT / "data/evaluation_metrics.csv")
        self.assertEqual(frame.shape, (9, 6))
        self.assertEqual(set(frame["Top %"]), {"5%", "10%", "20%"})
        for column in ["Precision@K", "Recall@K"]:
            self.assertTrue(frame[column].between(0, 1).all())
        self.assertTrue((frame["K"] > 0).all())
        self.assertTrue((frame["Lift"] >= 0).all())
        app = AppTest.from_file(str(ROOT / "pages/performance.py")).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(app.dataframe[-1].value.shape, (9, 6))
        self.assertEqual(set(app.dataframe[0].value["K"]), {1430})
        app.selectbox[0].set_value("5%").run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(set(app.dataframe[0].value["K"]), {715})

    def test_topk_validation(self):
        good = read_metrics(ROOT / "data/evaluation_metrics.csv")
        for column, value in [("Precision@K", 1.1), ("Recall@K", -1), ("K", 1.5), ("Lift", float("inf"))]:
            bad = good.copy()
            bad[column] = value
            with self.subTest(column=column), self.assertRaises(ValueError):
                read_metrics(io.StringIO(bad.to_csv(index=False)))
        with self.assertRaises(ValueError):
            read_metrics(io.StringIO(pd.concat([good, good]).to_csv(index=False)))

    def test_service_account_formats(self):
        info = {"type": "service_account", "client_email": "test@example.invalid"}
        for value in [info, json.dumps(info)]:
            with patch("data.st.secrets", {"gcp_service_account": value}), patch("data.service_account.Credentials.from_service_account_info") as credentials, patch("data.bigquery.Client") as bq:
                client()
                credentials.assert_called_once_with(info)
                bq.assert_called_once()

    def test_connection_error(self):
        with patch("data.client", side_effect=RuntimeError("secret must not show")):
            app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(app.error)
        self.assertNotIn("secret must not show", app.error[0].value)

if __name__ == "__main__":
    unittest.main()
