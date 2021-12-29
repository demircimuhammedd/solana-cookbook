---
title: Programs
head:
  - - meta
    - name: title
      content: Solana Cookbook | Program Recipes
  - - meta
    - name: og:title
      content: Solana Cookbook | Program Recipes
  - - meta
    - name: description
      content: Learn about Programs, Cross Program Invocation, Program Derived Address, more code Samples and Recipes at The Solana cookbook.
  - - meta
    - name: og:description
      content: Learn about Programs, Cross Program Invocation, Program Derived Address, more code Samples and Recipes at The Solana cookbook.
  - - meta
    - name: og:image
      content: https://solanacookbook.com/cookbook-sharing-card.png
  - - meta
    - name: og:image:alt
      content: Solana splash card
  - - meta
    - name: twitter:card
      content: summary
  - - meta
    - name: twitter:site
      content: "@solanacookbook"
  - - meta
    - name: twitter:image
      content: "https://solanacookbook.com/cookbook-sharing-card.png"
  - - meta
    - name: robots
      content: index,follow,noodp
  - - meta
    - name: googlebot
      content: index,follow
footer: MIT Licensed
---

# Programs

## How to get clock in a program

Getting a clock can be done in two ways

1. Passing `SYSVAR_CLOCK_PUBKEY` into an instruction
2. Accessing Clock directly inside an instruction.

It is nice to know both the methods, because some legacy programs still expect the `SYSVAR_CLOCK_PUBKEY` as an account.

### Passing Clock as an account inside an instruction

Let's create an instruction which receives an account for initializing and the sysvar pubkey

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/get-clock/method-one/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/get-clock/method-one/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

Now we pass the clock's sysvar public address via the client

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="TS" active>

  <template v-slot:default>

@[code](@/code/programs/get-clock/method-one/client/main.en.ts)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/get-clock/method-one/client/main.preview.en.ts)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

### Accessing Clock directly inside an instruction

Let's create the same instruction, but without expecting the `SYSVAR_CLOCK_PUBKEY` from the client side.

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/get-clock/method-two/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/get-clock/method-two/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

The client side instruction, now only needs to pass the state and payer accounts.

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="TS" active>

  <template v-slot:default>

@[code](@/code/programs/get-clock/method-two/client/main.en.ts)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/get-clock/method-two/client/main.preview.en.ts)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

## How to do Cross Program Invocation

A cross program invocation, is simply put calling another program's instruction inside our program. One best example to put forth is Uniswap's `swap` functionality. The `UniswapV2Router` contract, calls the necessary logic to swap, and calls the `ERC20` contract's transfer function to swap from one person to another. The same way, we can call a program's instruction to have multitude of purposes.

Lets have a look at our first example which is the `SPL Token Program's transfer` instruction. The required accounts we would need for a transfer to happen are

1. The Source Token Account (The account which we are holding our tokens)
2. The Destination Token Account (The account which we would be transferring our tokens to)
3. The Source Token Account's Holder (Our wallet address which we would be signing for)

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/cpi-transfer/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/cpi-transfer/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>
<br />
The corresponding client instruction would be as follows. For knowing the mint and token creation instructions, please refer to the full code nearby.
<br />
<br />
<SolanaCodeGroup>
  <SolanaCodeGroupItem title="TS" active>

  <template v-slot:default>

@[code](@/code/programs/cpi-transfer/client/main.en.ts)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/cpi-transfer/client/main.preview.en.ts)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

Now let's take a look at another example, which is `System Program's create_account` instruction. There is a slight difference between the above mentioned instruction and this. There, we never had to pass the `token_program` as one of the accounts inside the `invoke` function. However, there are exceptions where you are required to pass the invoking instruction's `program_id`. In our case it would be the `System Program's` program_id. ("11111111111111111111111111111111"). So now the required accounts would be

1. The payer account who funds the rent
2. The account which is going to be created
3. System Program account

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/cpi-transfer/program-system/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/cpi-transfer/program-system/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

The respective client side code will look as follows

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="TS" active>

  <template v-slot:default>

@[code](@/code/programs/cpi-transfer/client-system/main.en.ts)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/cpi-transfer/client-system/main.preview.en.ts)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

## Create a Program Derived Address

A Program Derived Addres is simply an account owned by the program, but has no private key. Instead it's signature is obtained by a set of seeds and a bump (a nonce which makes sure it's off curve). "**Generating**" a Program Address is different from "**creating**" it. One can generate a PDA using `Pubkey::find_program_address`. Creating a PDA essentially means to initialize the address with space and set the state to it. A normal Keypair account can be created outside of our program and then fed to initialize it's state. Unfortunately, for PDAs, it has be created on chain, due to the nature of not being able to sign on behalf of itself. Hence we use `invoke_signed` to pass the seeds of the PDA, along with the funding account's signature which results in account creation of a PDA.

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/create-pda/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/create-pda/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

One can send the required accounts via client as follows

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="TS" active>

  <template v-slot:default>

@[code](@/code/programs/create-pda/client/main.en.ts)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/create-pda/client/main.preview.en.ts)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

## Read account

Almost all instructions in Solana would require atleast 2 - 3 accounts, and they would be mentioned over the instruction handlers on what order it's expecting those set of accounts. It's fairly simple if we take advantage of the `iter()` method in Rust, instead of manually indicing the accounts. The `next_account_info` method basically slices the first index of the iterable and returning the account present inside the accounts array. Let's see a simple instruction which expects a bunch of accounts and requiring to parse each of them.

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/read-account/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/read-account/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>

## Verify Account

Since programs in Solana are stateless, we as a program creator have to make sure the accounts passed are validated as much as possible to avoid any malicious account entry. The basic checks one can do are

1. Check if the expected signer account has actually signed
2. Check if the expected state account's have been checked as writable
3. Check if the expected state account's owner is the called program id
4. If initializing the state for the first time, check if the account's already been initialized or not.
5. Check if any cross program ids passed (whenever needed) are as expected.

A basic instruction which initializes a hero state account, but with the above mentioned checks is defined below

<SolanaCodeGroup>
  <SolanaCodeGroupItem title="Rust" active>

  <template v-slot:default>

@[code](@/code/programs/verify-account/program/src/lib.rs)

  </template>

  <template v-slot:preview>

@[code](@/code/programs/verify-account/program/src/lib.preview.rs)

  </template>

  </SolanaCodeGroupItem>
</SolanaCodeGroup>
