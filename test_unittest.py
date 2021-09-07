import unittest  
import chatbot
import chatbotModel


class TestChatbot(unittest.TestCase):

    def test_clean_sentence(self):
        result = chatbot.clean_sentence("hello my name is Aaron")
        self.assertEqual(result, ['hello', 'my', 'name', 'is', 'aaron'])
    
    def test_bag_of_words(self):
        chatbot.bag_of_words("Can you please give me some tips on how to revise?")
    
    def test_prediction(self):
        chatbot.prediction("howdy!")
    
    def test_response(self):
        result = chatbot.response(chatbot.prediction("I'm having trouble making friends"), chatbot.intents)

if __name__ == '__main__':
    unittest.main()