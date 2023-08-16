# Collective Trust
Each voter simply  nominates one or more people; each person you nominate receives a share of your vote. 
Each vote is transitive; by nominating someone, each person they nominate also receives a slightly larger vote, and so on down the chain. 
People with the most total votes (directly nominated + transitive) are the elected representatives. 

The trustees you nominate directly each receive a share of half of your vote. 
So if you nominate three people, they will each receive a third of that half vote, i.e. 1/6th of your total vote. 
The people they nominate will receive their share of a quarter of your vote, and the nominees of those people receive a share of 1/8th of your vote, and so on. 
In this way, [all of these contributions throughout the chain of trust sum to 1](https://en.wikipedia.org/wiki/1/2_%2B_1/4_%2B_1/8_%2B_1/16_%2B_%E2%8B%AF) - your complete, single vote. \
The formula for the fraction of your vote contributed to any given person is described by the formula: 
```math
\begin{gather}
\text{contribution} = \frac{1}{\bar N 2^M} \\
\text{where $M$ is the degrees of seperation, and} \\
\bar N = N_1 N_2 N_3 \ldots N_M \\
\text{where $N$ is the number of nominees} \\
\text{each person has nominated}
\end{gather}
```
### Benefits to this system:
- Voting can be based on direct trust of people you know
- The transitive trust reflects the real communities and social networks people live in
- Candidates are not career politicians. This means any person with the trust of their community can be elected, not just those with the socio-economic means to choose politics as a career.
  - Political service is like jury duty. If you’re elected, you have to serve your term.
