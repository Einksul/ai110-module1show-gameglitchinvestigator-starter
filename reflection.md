# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  When starting the game, the number does not respect the stated range given by the difficulty. If the correct number is guessed in the first try the score is based on if you had clicked on 'new game'. Attempts
  where new game is not pressed results in a score of 70, and those that did resulted in 80. The final score logic also seems to be broken when wrong guesses are introduced. It is not consistent and vary even with
  when the same amount of incorrect guesses were used. The new game button does not work as intended. After finishing a game it does not restart all logic upon hitting the button. Subsequent guesses report that
  the game must be restarted even when the button had been pressed, it seems that clicking the new game button only regenerates the secret number. The hint logic reports the incorrect relation of the guess with the 
  secret number (i.e if guess g is less than the secret number n then it says go lower instead of higher and vice versa). Suprisingly if the guess is 100 the hint cycles between 'Higher' and 'Lower' regardless of
  the secret number. invalid inputs (e.g letters or empty inputs) are correctly indentified and give an error but still decrement the attempts counter, which uses up attempts and cna lead to negative attempt values.
  I assume that this error could be the underlying cause of the misbehaving scores.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
