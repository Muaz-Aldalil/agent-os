# Execution Transparency & Status Reporting Protocol

## Purpose
Prevent the human operator from experiencing unexpected silence, apparent freezing, or ambiguity regarding agent activity during background tasks or network disruptions.

---

## 1. Background Task Transparency
Whenever initiating or waiting on an asynchronous command or background task (such as test suites, production builds, long migrations, or package installations), the agent MUST output an explicit status message before concluding the turn:

> ⏳ **Running Background Tasks/Tests:** `[Command or Test Suite Description]` — *Awaiting process completion...*

The agent must NEVER conclude a turn in silence while a background task is running.

---

## 2. Network Disruption & Reconnection Protocol
Whenever recovering from a network drop, connection abort, socket reset, or DNS lookup failure (`wsarecv`, `no such host`, etc.), the agent MUST immediately open its response with an explicit acknowledgment:

> ⚠️ **Internet Disconnected / Connection Re-established:** *Resuming execution from [last active step]...*

---

## 3. Scope
This protocol is permanent, global, and mandatory across all workspaces and conversations.
