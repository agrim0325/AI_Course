# Bayesian Networks and Autoregressive Language Models - Lab Report

## Question 1: Why is this decomposition useful for generating text?
The autoregressive decomposition uses the chain rule to break down the complex joint probability of an entire sequence P(X_1, \dots, X_T) into a product of simpler conditional probabilities P(X_t | X_1, \dots, X_{t-1}). This is incredibly useful for generating text because it gives us a step-by-step sequential recipe: we can generate the first word, then generate the second word conditioned on the first, and so on, sampling from left to right.

## Question 2: What independence assumption is being made by this network?
The first-order Markov assumption assumes that each word only depends on the immediately preceding word, and is conditionally independent of all other previous words given that immediate predecessor. 
In probability notation: P(X_t | X_1, \dots, X_{t-1}) \approx P(X_t | X_{t-1}).

## Question 3: Construct the conditional probability distribution
Given the dataset:
- 	he: followed by cat (3), dog (3), mat (2), ug (2), park (2). Total = 12.
  - P(\text{cat} | \text{the}) = 3/12 = 0.25
  - P(\text{dog} | \text{the}) = 3/12 = 0.25
  - P(\text{mat} | \text{the}) = 2/12 \approx 0.167
  - P(\text{rug} | \text{the}) = 2/12 \approx 0.167
  - P(\text{park} | \text{the}) = 2/12 \approx 0.167
- cat: followed by sat (2), an (1). Total = 3.
  - P(\text{sat} | \text{cat}) = 2/3 \approx 0.667
  - P(\text{ran} | \text{cat}) = 1/3 \approx 0.333
- dog: followed by sat (2), an (1). Total = 3.
  - P(\text{sat} | \text{dog}) = 2/3 \approx 0.667
  - P(\text{ran} | \text{dog}) = 1/3 \approx 0.333
- sat: followed by on (4). Total = 4.
  - P(\text{on} | \text{sat}) = 4/4 = 1.0
- an: followed by 	o (2). Total = 2.
  - P(\text{to} | \text{ran}) = 2/2 = 1.0

*Zero-probability transitions:* Transitions that never occur in the dataset have probability 0, such as P(\text{dog} | \text{cat}) = 0 or P(\text{the} | \text{the}) = 0.

## Question 4: Where in the program are the transition counts stored?
In the Python code, transition counts are stored in a nested dictionary named self.transitions. For example, self.transitions[current_word][next_word] holds the count.

## Question 5: Where is P(X_t | X_{t-1}) computed?
It is computed in the _train() method where we iterate over the counts, sum the occurrences for a given context to get the 	otal, and then divide each count by the 	otal to populate the self.probabilities dictionary.

## Question 6: How does the program choose the next word?
The program supports both!
- In generate_greedy(), it always chooses the most probable word by using max() on the probabilities (greedy generation).
- In generate_sample(), it samples from the probability distribution using andom.choices(..., weights=probs) (probabilistic generation).
*Difference:* Greedy generation is deterministic and will always produce the exact same sequence given the same starting word. Sampling respects the distribution, so words with a 25% probability will be chosen roughly 25% of the time, allowing for diverse generated text.

## Question 7: What happens if the program encounters a word for which no transition has been observed?
If a word has no observed transitions, the dictionary lookup will fail (or return empty). In the implementation, I added a check if current_word not in self.probabilities: which breaks the generation loop, effectively halting the sequence.

## Question 8: If one of the totals is 0.87, what does this tell you about the implementation?
A total of 0.87 means the probabilities do not sum to 1. This indicates a bug in the implementation, likely an error in counting the frequencies or dividing by the wrong denominator when normalizing the conditional probability table (CPT).

## Question 9: Are the most probable predictions always the same as the words that you would personally expect?
Not necessarily. The probability model only strictly reflects the statistical frequencies of the limited training corpus. Human linguistic expectations draw upon a vast semantic and syntactic understanding of the world, whereas this simple model merely repeats whatever n-grams were most common in the 6 sentences it read.

## Question 10: Compare the two sets of generated sentences. Which mode produces more variation? Why?
The **Sampling mode** produces much more variation. The **Greedy mode** always outputs exactly the same sentence—in fact, our tests show that because <START> -> 	he -> cat -> sat -> on -> 	he -> cat, greedy generation gets stuck in an **infinite deterministic loop** (	he cat sat on the cat sat on...) and never reaches the <END> token! Sampling probabilistically explores different branches, generating diverse valid sentences from the dataset and avoiding deterministic loops.

## Question 11: How does the second-order model differ from the first-order model?
1. **Graph structure:** Instead of a simple chain X_{t-1} \to X_t, each node now has two parents: X_{t-2} \to X_t and X_{t-1} \to X_t.
2. **Conditional probability table:** The CPT is conditioned on pairs of words (bigrams) rather than single words (unigrams), making it significantly larger.
3. **Amount of context available:** It has twice the context (2 previous words instead of 1), allowing it to capture longer-range dependencies (like knowing a noun phrase started a few words ago).
4. **Amount of data needed:** It needs exponentially more data. Because the number of possible word pairs is the square of the vocabulary size, the model will suffer from data sparsity (many pairs will have 0 observations) unless provided with a much larger corpus.

## Question 12: Why does increasing the amount of context potentially improve prediction? Why can it make it harder to estimate from limited data?
More context improves prediction because language has long-term dependencies; knowing two previous words provides much more grammatical and semantic clue than just one word. 
However, it makes estimation harder because the CPT grows exponentially with the context size. If vocabulary is V, a first-order model has V^2 parameters, but a second-order model has V^3 parameters. In limited data, most V^3 combinations will never appear, leading to zero-probabilities for perfectly valid contexts (data sparsity/overfitting).

## Question 13: Why is Approach B preferable when constructing an intelligent system?
Approach B ("Implement the following probabilistic model...") is preferable because:
- **Specifying intended behaviour:** It formalizes exactly what the system is mathematically supposed to do, rather than hoping the LLM guesses right.
- **Understanding representation:** It forces the engineer to understand that the model uses a CPT and transition counts.
- **Validating / Testing invariants:** Because the math is explicitly defined, we can write unit tests (e.g. checking that probabilities sum to 1).
- **Distinguishing implementation from model:** It separates the abstract probabilistic model from the Python code used to execute it. If the code has a bug, we can check it against the math.

## Question 14: What did thinking of the language model as a Bayesian network give you?
Thinking of it as a Bayesian network provided:
- **A factorisation of the joint distribution:** It showed how an impossibly large joint probability of an entire sentence can be tractably broken down into small conditional pieces.
- **A representation of dependencies:** The DAG structure visually and mathematically clarified exactly which previous words influence the current word (the Markov assumption).
- **A principled method for generation:** It gave a mathematically sound algorithm for generating sequences (ancestral sampling) by traversing the graph from left to right.
- **A way to understand the effect of increasing context:** By changing the graph structure (adding an arrow from X_{t-2}), the theoretical and practical differences between a first-order and second-order model became incredibly clear.
