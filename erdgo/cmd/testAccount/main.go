package main

import (
	"fmt"

	"github.com/ElrondNetwork/elrond-sdk/erdgo"
)

func main() {
	ep := erdgo.NewElrondProxy("http://localhost:8079")

	// Retrieving network configuration parameters
	networkConfig, err := ep.GetNetworkConfig()
	if err != nil {
		fmt.Printf("Error getting network config: %s\n\r", err)
		return
	}

	address := "erd18yddfyzyskajjteyj90ueackpcsp9set2ma8vp54cj4zh54hjussukc6mu"
	// Retrieve account info from the network (balance, nonce)
	accountInfo, err := ep.GetAccount(address)
	if err != nil {
		fmt.Printf("Error retrieving account info: %s\n\r", err)
		return
	}
	floatBalance, err := accountInfo.GetBalance(networkConfig.Denomination)
	if err != nil {
		fmt.Printf("Unable to compute balance: %s\n\r", err)
		return
	}

	fmt.Printf("Address: %s\n\rBalance: %.6f eGLD\n\rNonce: %v\n\r",
		address, floatBalance, accountInfo.Nonce)
}
