import warnings

# Ignore RequestsDependencyWarning
warnings.filterwarnings("ignore", category=UserWarning, module="requests")

# Imports for wallet creation and colored output
from web3 import Web3
from eth_account import Account
import json
import os
from colorama import Fore, Style, init
from solana.keypair import Keypair
import base58
from InquirerPy import inquirer

# Initialize colorama
init(autoreset=True)

# Main function to create wallets
def create_wallets():
    # Ask for the type of wallet to create
    print(Fore.CYAN + "Welcome! This script will help you create EVM or Solana wallets.")
    
    wallet_type = inquirer.select(
        message="Which type of wallet would you like to create?",
        choices=["EVM", "Solana"],
        default="EVM",
    ).execute().lower()
    
    # Ask for the number of wallets to create
    try:
        num_wallets = int(input(Fore.YELLOW + "How many wallets would you like to create? " + Fore.RESET))
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter a number.")
        return

    # Create the folder for storing data
    os.makedirs('wallets', exist_ok=True)

    private_keys = []
    addresses = []
    seeds = []  # Using private key as a substitute for seed

    # Creating wallets
    print(Fore.GREEN + f"\nCreating {num_wallets} {wallet_type.upper()} wallets...\n")

    for i in range(num_wallets):
        if wallet_type == "evm":
            # Create a new EVM wallet
            acct = Account.create()

            # Add the private key to the list
            private_keys.append(acct.key.hex())

            # Add the address to the list
            addresses.append(acct.address)

            # Add the seed (using the private key here as a substitute)
            seeds.append(acct.key.hex())

            # Print wallet details for reference (optional)
            print(Fore.BLUE + f"EVM Wallet {i + 1}:")
            print(Fore.MAGENTA + f"  Address: {acct.address}")
            print(Fore.MAGENTA + f"  Private Key: {acct.key.hex()}\n")

        elif wallet_type == "solana":
            # Create a new Solana wallet
            keypair = Keypair.generate()

            # Get the private key in Base58 format
            private_key_base58 = base58.b58encode(keypair.secret_key).decode('utf-8')
            private_keys.append(private_key_base58)

            # Get the public address (also in Base58 format)
            address = str(keypair.public_key)
            addresses.append(address)

            # Using the private key as a substitute for seed
            seeds.append(private_key_base58)

            # Print wallet details for reference (optional)
            print(Fore.BLUE + f"Solana Wallet {i + 1}:")
            print(Fore.MAGENTA + f"  Address: {address}")
            print(Fore.MAGENTA + f"  Private Key (Base58): {private_key_base58}\n")

    # Save private keys to a separate file
    with open(f'wallets/{wallet_type}_private_keys.json', 'w') as pk_file:
        json.dump(private_keys, pk_file, indent=4, ensure_ascii=False)

    # Save addresses to a separate file
    with open(f'wallets/{wallet_type}_addresses.json', 'w') as addr_file:
        json.dump(addresses, addr_file, indent=4, ensure_ascii=False)

    # Save seeds to a separate file (using private keys as substitutes)
    with open(f'wallets/{wallet_type}_seeds.json', 'w') as seeds_file:
        json.dump(seeds, seeds_file, indent=4, ensure_ascii=False)

    # Success message
    print(Fore.GREEN + Style.BRIGHT + f"\n{num_wallets} {wallet_type.upper()} wallets have been successfully created and the information has been stored in the 'wallets' folder.")
    print(Fore.CYAN + "Please make sure to keep the private keys secure!")

# Run the function
if __name__ == "__main__":
    create_wallets()
