small commits!! so you can easily roll back

feature and bug fixes should be separate


claude made a mistake with the attmepts logic first we tried to fix the game over message appearing when there was one attempt left. This fix broke coutning logic and allowed for one more attempt then usual.
We eventually came to the idea that all the logic code should run before rendering the page. 
