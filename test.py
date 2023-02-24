try:
    from app import view_room
    import unittest
except Exception as e:
    print("Some things are missing {}". format(e))
    
class FlaskTest(unittest.TestCase):
    #check for response 200
    def test_view(self):
        test = view_room(self)
        response = test.get('/rooms/<room_id>')
        statuscode = response.status_code
        self.assertEquals(statuscode, 200)
        
if __name__ == "__main__":
    unittest.main()