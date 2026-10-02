import random
from collections import defaultdict

sentences = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

def tokenize(sentences):
    tokenized = []
    for s in sentences:
        tokens = ['<START>'] + s.lower().split() + ['<END>']
        tokenized.append(tokens)
    return tokenized

class FirstOrderModel:
    def __init__(self, data):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.probabilities = defaultdict(dict)
        self._train(data)

    def _train(self, data):
        for sentence in data:
            for i in range(len(sentence) - 1):
                current_word = sentence[i]
                next_word = sentence[i+1]
                self.transitions[current_word][next_word] += 1
        
        for current_word, next_words in self.transitions.items():
            total = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[current_word][next_word] = count / total

    def check_probabilities(self):
        print("Checking probability sums (First-order):")
        for word, next_probs in self.probabilities.items():
            total = sum(next_probs.values())
            print(f"{word}: {total:.2f}")

    def predict_next(self, current_word):
        if current_word not in self.probabilities:
            return None
        return self.probabilities[current_word]
        
    def generate_greedy(self):
        sentence = ['<START>']
        while sentence[-1] != '<END>':
            current_word = sentence[-1]
            if current_word not in self.probabilities:
                break
            
            next_probs = self.probabilities[current_word]
            best_word = max(next_probs, key=next_probs.get)
            sentence.append(best_word)
            
            if len(sentence) > 20: 
                break
        return " ".join(sentence)

    def generate_sample(self):
        sentence = ['<START>']
        while sentence[-1] != '<END>':
            current_word = sentence[-1]
            if current_word not in self.probabilities:
                break
                
            next_probs = self.probabilities[current_word]
            words = list(next_probs.keys())
            probs = list(next_probs.values())
            
            next_word = random.choices(words, weights=probs, k=1)[0]
            sentence.append(next_word)
            
            if len(sentence) > 20: 
                break
        return " ".join(sentence)

class SecondOrderModel:
    def __init__(self, data):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.probabilities = defaultdict(dict)
        self._train(data)

    def _train(self, data):
        for sentence in data:
            padded_sentence = ['<START>'] + sentence
            for i in range(len(padded_sentence) - 2):
                context = (padded_sentence[i], padded_sentence[i+1])
                next_word = padded_sentence[i+2]
                self.transitions[context][next_word] += 1
        
        for context, next_words in self.transitions.items():
            total = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[context][next_word] = count / total
                
    def check_probabilities(self):
        print("\nChecking probability sums (Second-order):")
        for context, next_probs in self.probabilities.items():
            total = sum(next_probs.values())
            print(f"{context}: {total:.2f}")

    def generate_sample(self):
        sentence = ['<START>', '<START>']
        while sentence[-1] != '<END>':
            context = (sentence[-2], sentence[-1])
            if context not in self.probabilities:
                break
                
            next_probs = self.probabilities[context]
            words = list(next_probs.keys())
            probs = list(next_probs.values())
            
            next_word = random.choices(words, weights=probs, k=1)[0]
            sentence.append(next_word)
            
            if len(sentence) > 20: 
                break
        return " ".join(sentence[1:]) 

def run_lab():
    tokenized_data = tokenize(sentences)
    
    print("--- First Order Model ---")
    model1 = FirstOrderModel(tokenized_data)
    model1.check_probabilities()
    
    print("\nNext word predictions:")
    for w in ["the", "cat", "dog", "sat", "ran"]:
        probs = model1.predict_next(w)
        print(f"P(* | {w}) = {probs}")
        if probs:
            best = max(probs, key=probs.get)
            print(f"arg max P(w | {w}) = {best}")
            
    print("\nGreedy Generation (5 sentences):")
    for _ in range(5):
        print(model1.generate_greedy())
        
    print("\nSampling Generation (20 sentences):")
    for _ in range(20):
        print(model1.generate_sample())
        
    print("\n--- Second Order Model ---")
    model2 = SecondOrderModel(tokenized_data)
    model2.check_probabilities()
    
    print("\nSampling Generation (5 sentences):")
    for _ in range(5):
        print(model2.generate_sample())

if __name__ == "__main__":
    run_lab()
