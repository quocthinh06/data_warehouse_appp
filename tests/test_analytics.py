import unittest
from unittest.mock import Mock
from types import SimpleNamespace
import pandas as pd
from google.api_core.exceptions import NotFound, BadRequest
from analytics import cohort, profile_sql, load_profiles, PROFILE_FIELDS
from data import REQUIRED
import charts

FIELDS = REQUIRED | {"prediction_date"}

class AnalyticsTests(unittest.TestCase):
    def test_cohort_parameterization(self):
        where, params = cohort(FIELDS, True, ["Cao' OR TRUE"], .6)
        self.assertNotIn("Cao' OR TRUE", where)
        self.assertIn("@levels", where)
        self.assertIn("@minimum", where)
        self.assertEqual({p.name: p for p in params}["minimum"].value, .6)

    def test_join_requires_both_keys_and_unique_match(self):
        sql, _ = profile_sql(FIELDS, PROFILE_FIELDS, True, ["Cao"], 0)
        self.assertIn("p.patient_nbr AS STRING) = w.patient_key", sql)
        self.assertIn("p.encounter_id AS STRING) = w.encounter_key", sql)
        self.assertIn("GROUP BY patient_key, encounter_key", sql)
        self.assertIn("WHERE key_rows = 1", sql)
        self.assertIn("'ambiguous'", sql)
        self.assertIn("'unmatched'", sql)
        self.assertNotIn("SELECT * FROM", sql)
        for column in PROFILE_FIELDS:
            partial, _ = profile_sql(FIELDS, {column}, True, ["Cao"], 0)
            self.assertIn("AS " + column, partial)

    def test_optional_metadata_unavailable(self):
        bq = Mock()
        bq.get_table.side_effect = NotFound("missing")
        frame, reason = load_profiles(bq, FIELDS, "US", True, ["Cao"], 0)
        self.assertIsNone(frame)
        self.assertIn("wide_table", reason)
        bq.query.assert_not_called()

    def test_optional_wrong_location_or_keys(self):
        bq = Mock()
        bq.get_table.return_value = SimpleNamespace(location="EU", schema=[SimpleNamespace(name=n) for n in PROFILE_FIELDS | {"patient_nbr", "encounter_id"}])
        frame, reason = load_profiles(bq, FIELDS, "US", True, ["Cao"], 0)
        self.assertIsNone(frame)
        self.assertIn("khác vùng", reason)
        bq.query.assert_not_called()
        bq.get_table.return_value = SimpleNamespace(location="US", schema=[])
        frame, reason = load_profiles(bq, FIELDS, "US", True, ["Cao"], 0)
        self.assertIn("đủ", reason)

    def test_profile_api_failure_logs_diagnostic_without_displaying_it(self):
        bq = Mock()
        bq.get_table.return_value = SimpleNamespace(location="US", schema=[SimpleNamespace(name=n) for n in PROFILE_FIELDS | {"patient_nbr", "encounter_id"}])
        bq.query.side_effect = BadRequest("Diagnostic SQL message for server log only")
        with self.assertLogs("analytics", level="ERROR") as logs:
            frame, reason = load_profiles(bq, FIELDS, "US", True, ["Cao"], 0)
        self.assertIsNone(frame)
        self.assertIn("PROFILE_QUERY_ERROR", reason)
        self.assertNotIn("Diagnostic SQL message", reason)
        self.assertIn("Diagnostic SQL message", logs.output[0])
        self.assertIn("BadRequest", logs.output[0])

    def test_chart_specs(self):
        distribution = pd.DataFrame([dict(risk_level="Cao", prediction_count=5, share=.5)])
        histogram = pd.DataFrame([dict(risk_level="Cao", prediction_count=5, score_start=.5, score_end=.55)])
        factors = pd.DataFrame([dict(factor="number_inpatient", label="Nhập viện trước", prediction_count=5)])
        profile = pd.DataFrame([dict(risk_level="Cao", category="[50-60)", prediction_count=5, avg_score=.6)])
        for chart in [charts.donut(distribution), charts.histogram(histogram), charts.factors(factors), charts.profile(profile), charts.profile(profile, True)]:
            self.assertTrue(chart.to_dict(validate=True)["encoding"])

if __name__ == "__main__":
    unittest.main()
