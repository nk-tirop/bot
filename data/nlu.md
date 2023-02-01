version: "2.0"

nlu:
## intent: greet
  examples: |
    - hey
    - hello
    - hi
    - hello there
    - good morning
    - good evening
    - moin
    - hey there
    - let's go
    - hey dude
    - goodmorning
    - goodevening
    - good afternoon

## intent: affirm
  examples: |
    - yes
    - y
    - indeed
    - of course
    - that sounds good
    - correct

## intent: deny
  examples: |
    - no
    - n
    - never
    - I don't think so
    - don't like that
    - no way
    - not really

## intent: no_internet
  - I have no_internet connection
  - My internet is not working
  - I can't access the internet
  - My internet is down
  - I am not able to connect to the internet
  - My internet is not working
  - I am having trouble with my internet connection
  - I am unable to access the internet
  - My router is not providing internet access
  - I am not getting any internet on my device
  
## intent: router_number
  - my router number is [98235](router_number) 
  - it is [23456](router_number)
  - the number is [12345](router_number)
  - my number is [67890](router_number)

## intent: give_time
  - what is the time
  - tell me the time
  - get the time
  - can you tell me what time it is