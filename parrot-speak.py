# markov_chains.py
"""
    How to talk like a parrot: Markov Chains.

    Hayden Parkinson

"""

import numpy as np
from scipy import linalg as la

class Parrot(object):
    """Markov chain creator for simulating Parrot-speak.

    Attributes:
        transition ((n+2,n+2) ndarray): A transition matrix from each word
            the next possible words

        states ((n+2) ndarray): A list of strings corresponding to the indecies
            of the transition matrix

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print(yoda.babble())
        The dark side of loss is a path as one with you.
    """
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. The file must be formatted to have one complete sentence
        on each line.
        """

        with open(filename, 'r') as my_file:

            data = my_file.read()

            # Count the number of unique words in the entire file,
            n = len(set(data.split()))

            # Build a square array of zeroes of that size + 2, (n + start/stop states)
            transition = np.zeros((n+2,n+2))

            # Initialize a list of states, beginning with '$tart'
            states = ['$tart']
            tracked_words = set(states)

            sentences = data.split('\n')
            for i, s in enumerate(sentences):
                # Skip any empty lines
                if len(s) == 0:
                    continue

                # split sentence into words, add any 'new' words to states list
                words = s.split()

                # Add untracked words to the states list
                for word in words:
                    if word not in tracked_words:
                        states.append(word)
                        tracked_words.add(word)

                # Add a connection from word x to word x+1 in words
                # REMEMBER: the matrix is setup in the form
                # transition['to this word', 'from this word']


                transition[states.index(words[0]),0] += 1

                for x in range(len(words)-1):
                    to = states.index(words[x+1])
                    fr = states.index(words[x])
                    transition[to,fr] += 1

                transition[-1,states.index(words[-1])] += 1

            # Make sure the stop state transitions to itself
            transition[-1,-1] = 1
            states.append('$top')

            # Normalize the columns of transition
            for i in range(len(transition)):
                transition[:,i] = transition[:,i] / sum(transition[:,i])

            self.transition = transition
            self.states = states



    def speak(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        # current_state starts at '$tart'
        current_state = 0
        path = []

        while True:
            outcome = np.random.multinomial(1, self.transition[:,current_state])
            current_state = np.argmax(outcome)
            if current_state == len(self.transition) - 1:
                break
            path.append(current_state)

        sentence = [self.states[x] for x in path]
        return ' '.join(sentence)

if __name__ == '__main__':
    polly = Parrot('yoda.txt')
    polly.speak()
    polly.speak()
    polly.speak()
