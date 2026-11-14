import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from data_model import sample_data, validate_frame

class DashboardTests(unittest.TestCase):
    def test_pages_and_records(self):
        at=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=20).run()
        self.assertFalse(at.exception)
        for key in ['sleep','medical','exercise','nutrition','wellbeing','eva']:
            at.button(key='nav_'+key).click().run()
            self.assertFalse(at.exception)
            self.assertGreaterEqual(len(at.metric),2)
        at.button(key='nav_wellbeing').click().run()
        at.slider[0].set_value(4)
        at.text_area[0].input('Feeling ready')
        [b for b in at.button if b.label=='Save check-in'][0].click().run()
        self.assertEqual(len(at.session_state['records']),1)
        self.assertEqual(at.session_state['records'][0]['mood'],4)
        at.checkbox[0].check().run()
        self.assertTrue(any(at.session_state['done'].values()))
        [b for b in at.button if b.label=='Data & exports'][0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.get('download_button')),3)
        at.radio[0].set_value('Upload CSV').run()
        self.assertFalse(at.exception)
    def test_validation(self):
        self.assertEqual(len(sample_data()),504)
        for bad in ['unit','duplicate','numeric','timestamp','empty']:
            with self.subTest(case=bad):
                df=sample_data().head(2).copy()
                if bad=='unit':df.loc[0,'unit']='wrong'
                if bad=='duplicate':df=df.iloc[[0,0]]
                if bad=='numeric':df.loc[0,'value']=float('inf')
                if bad=='timestamp':df.loc[0,'timestamp']=None
                if bad=='empty':df=df.iloc[:0]
                with self.assertRaises(ValueError):validate_frame(df)
    def test_map_event_navigation(self):
        at=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=20).run()
        at.session_state['base_map']={'zone':'sleep','event':123}
        at.run()
        self.assertFalse(at.exception)
        self.assertEqual(at.session_state['page'],'sleep')
if __name__=='__main__':unittest.main()
