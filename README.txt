🔐 Crypto-Blockchain
A complete Python-based blockchain prototype demonstrating core concepts of decentralized ledgers, wallets, and block validation. This project is structured modularly with dedicated folders for blockchain logic, UI components, and utility scripts.

🔧 Features

Custom Blockchain Engine (Blockchain/): Handles blocks, mining, consensus, and validation.

Wallet Simulation: Simulates users with wallet files and transaction history.

Proof-of-Work and block hashing using SHA-256.

Text-based UI (ui/) for simple interaction or visualization.

Persistence: Chains and wallets saved to .txt files (e.g., blockchain-5000.txt, wallet-5000.txt).

Utility Scripts for cryptographic or chain functions.

📁 Project Structure
Blockchain/     - Core blockchain logic (block, chain, mining, validation)
ui/             - Interface layer for interacting with the chain
utility/        - Helper modules (e.g., hash generators, validators)
wallet-*.txt    - Simulated wallet data for users
blockchain-*.txt- Stored blockchain data (per port/user)
demo.txt        - Example data or usage reference
