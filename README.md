# CongestRL: Reinforcement Learning Congestion Control in Virtual Network Simulation


This project was made for the Computational Intelligence & Deep Reinforcement Learning course of ECE AuTH.
As part of it, a parrelizable virtual netwrok consisting of routers that exchange packets was implemented.
The goal is to maintain congestion, meaning the amount of packets on flight, below a congestion limit while also
keeping the delay times of packets as low as possible. For this, a baseline Rnadom policy was implemented, along with
a DQN and PPO agent, with 3 different reward functions for testing.

Examples of execution scenarios can be found in the [tests.integration](tests/integration) module.

[View the full report (PDF)](report.pdf)
