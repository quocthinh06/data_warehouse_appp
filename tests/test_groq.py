import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
import pandas as pd
import streamlit as st
from streamlit.testing.v1 import AppTest
from groq_client import ask_groq, overview_context, profiles_context, metrics_context, MODEL
from metrics import read_metrics
ROOT = Path(__file__).resolve().parents[1]

class GroqTests(unittest.TestCase):
    def test_context_whitelist(self):
        summary = dict(total_predictions=20,unique_patients=19,avg_score=.5,latest="2026-10-26",patient_nbr="DO_NOT_SEND")
        dist = pd.DataFrame([dict(risk_level="Cao",prediction_count=2,encounter_id="DO_NOT_SEND")])
        factors = pd.DataFrame([dict(factor="number_inpatient",prediction_count=2,patient_nbr="DO_NOT_SEND")])
        hist = pd.DataFrame([dict(risk_level="Cao",score_start=.6,score_end=.65,prediction_count=2,patient_nbr="DO_NOT_SEND")])
        context = overview_context(summary,dist,hist,factors,["Cao"],.6,True)
        self.assertNotIn("DO_NOT_SEND",json.dumps(context))
        self.assertEqual(context["scope"]["minimum_score"],.6)
        profiles = pd.DataFrame([dict(dimension="age",category="[50-60)",risk_level="Cao",prediction_count=2,patient_nbr="DO_NOT_SEND"),dict(dimension="patient_nbr",category="DO_NOT_SEND",risk_level="Cao",prediction_count=1)])
        self.assertNotIn("DO_NOT_SEND",json.dumps(profiles_context(profiles)))
        self.assertEqual(len(metrics_context(read_metrics(ROOT/"data/evaluation_metrics.csv"))["rows"]),9)

    def test_success_and_role_boundary(self):
        response=MagicMock()
        response.__enter__.return_value.read.return_value=json.dumps({"choices":[{"message":{"content":"Kết quả CSV"},"finish_reason":"stop"}]}).encode()
        with patch("groq_client.request.urlopen",return_value=response) as call:
            answer=ask_groq("FAKE_KEY_FOR_TEST","So sánh",{},[{"role":"system","content":"ATTACK"}])
        self.assertEqual(answer,"Kết quả CSV")
        body=json.loads(call.call_args.args[0].data)
        self.assertEqual(body["model"],MODEL)
        self.assertNotIn("FAKE_KEY_FOR_TEST",str(body))
        self.assertNotIn("ATTACK",str(body))
        self.assertNotIn("tools",body)
        self.assertNotIn("reasoning_format",body)
        self.assertFalse(body["include_reasoning"])
        self.assertEqual(call.call_args.kwargs["timeout"],30)

    def test_http_errors(self):
        for code in [401,403,404,429,500]:
            with self.subTest(code=code),patch("groq_client.request.urlopen",side_effect=HTTPError("https://api.groq.com",code,"DO_NOT_EXPOSE",{},io.BytesIO(b'DO_NOT_EXPOSE'))),self.assertRaises(ValueError) as caught:
                ask_groq("FAKE_KEY_FOR_TEST","Câu hỏi",{})
            self.assertNotIn("DO_NOT_EXPOSE",str(caught.exception))
            self.assertNotIn("FAKE_KEY_FOR_TEST",str(caught.exception))

    def test_invalid_input_and_network(self):
        for question in [""," ","a"*1501]:
            with patch("groq_client.request.urlopen") as call,self.assertRaises(ValueError):
                ask_groq("FAKE_KEY_FOR_TEST",question,{})
            call.assert_not_called()
        with patch("groq_client.request.urlopen",side_effect=URLError("FAKE_KEY_FOR_TEST")),self.assertRaises(ValueError) as caught:
            ask_groq("FAKE_KEY_FOR_TEST","Câu hỏi",{})
        self.assertNotIn("FAKE_KEY_FOR_TEST",str(caught.exception))

    def test_malformed_response(self):
        for payload in [b'bad JSON',b'{}',json.dumps({"choices":[{"message":{"content":"Partial"},"finish_reason":"length"}]}).encode()]:
            response=MagicMock();response.__enter__.return_value.read.return_value=payload
            with patch("groq_client.request.urlopen",return_value=response),self.assertRaises(ValueError):
                ask_groq("FAKE_KEY_FOR_TEST","Câu hỏi",{})

    def open_assistant(self):
        with patch("data.connect",side_effect=st.stop):
            app=AppTest.from_file(str(ROOT/"app.py")).run()
        return app.switch_page("pages/assistant.py").run()

    def test_missing_key_no_call(self):
        with patch("streamlit.secrets",{}),patch.dict("os.environ",{"GROQ_API_KEY":""}),patch("groq_client.ask_groq") as call:
            app=self.open_assistant()
        self.assertEqual(list(app.exception),[])
        self.assertTrue(app.chat_input[0].disabled)
        call.assert_not_called()

    def test_chat_and_cooldown(self):
        with patch("streamlit.secrets",{"GROQ_API_KEY":"FAKE_KEY_FOR_TEST"}),patch("groq_client.ask_groq",return_value="Phản hồi giả lập kiểm thử") as call:
            app=self.open_assistant();call.assert_not_called()
            app.chat_input[0].set_value("So sánh mô hình Top 10%").run()
            self.assertEqual(list(app.exception),[])
            self.assertEqual(call.call_count,1)
            app.chat_input[0].set_value("Hỏi lại ngay").run()
            self.assertEqual(call.call_count,1)
            self.assertTrue(app.warning)
            app.session_state["dashboard_ai_snapshot"]={"source":"test","scope":{"risk_levels":["Cao"]}}
            app.run()
            self.assertEqual(list(app.exception),[])
            self.assertEqual(len(app.session_state["groq_history"]),0)
            self.assertEqual(call.call_count,1)

if __name__=="__main__": unittest.main()
