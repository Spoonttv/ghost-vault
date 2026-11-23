# Ghost Vault

**A secrets vault guarded by agents, with split keys and decoys.**

*A project by Glava Volya (Spoon)*

Ghost Vault protects sensitive data with three principles, combined in a new way:

## 1. Two keys out of three
The master key is split into three shares. Two are needed to open the vault, and a single share reveals nothing. No one can open it alone. The same mechanism also lets you pass access on to someone you trust.

## 2. Decoys that are real vaults
Around the real server sit indistinguishable copies, each with its own encryption and fake data. Breaking a decoy reveals nothing about the mother server, and any contact raises the alarm.

## 3. Agents that guard without being able to read
Local AI agents watch every access and flag anything suspicious, while never holding a key or any data.

## Current status
A prototype running on a personal server (Proxmox), with OpenBao for the vault, OpenCanary for the decoys, and Ollama for the agents. Fake data only. The cryptography relies on proven open-source libraries, never on home-made code.

## What's next
Make the decoys perfectly indistinguishable from the real server, and design the vault from the ground up to resist future quantum computers.
