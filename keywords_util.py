from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage
import matplotlib.pyplot as plt

chat = ChatAnthropic(model='claude-2')

doc = """
    Supervised learning is the machine learning task of learning a function that
    maps an input to an output based on example input-output pairs. It infers a
    function from labeled training data consisting of a set of training examples.
    In supervised learning, each example is a pair consisting of an input object
    (typically a vector) and a desired output value (also called the supervisory signal). 
    A supervised learning algorithm analyzes the training data and produces an inferred function, 
    which can be used for mapping new examples. An optimal scenario will allow for the 
    algorithm to correctly determine the class labels for unseen instances. This requires 
    the learning algorithm to generalize from the training data to unseen situations in a 
    'reasonable' way (see inductive bias).
"""
def extract_key_words(doc):
  messages = [
      HumanMessage(
          content=f"""
          <p>
          {doc}
          </p>

          <Question> Can you give me the keywords in the above paragraph?
          Just provide the list of keywords as a comma-separated list and nothing else.
          There should be no more than 3 keywords. Pick out the best ones.
          </Question>
          """
      )
  ]

  keywords = (chat(messages).content).split(", ")
  return keywords


def plot_key_words(word_counts):
  sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))
  plt.bar(sorted_word_counts.keys(), sorted_word_counts.values())
  plt.xlabel('Words')
  plt.ylabel('Counts')
  plt.title('Word Frequency')
  plt.xticks(rotation=45)
  plt.tight_layout()  # To prevent labels from being cut off
  plt.show()
  return keywords

def main():
  keywords = extract_key_words(doc)
  word_counts = {}
  for word in keywords:
    word_counts[word] = 1

  print(keywords)
  plot_key_words(word_counts)

if __name__ == "__main__":
  main()