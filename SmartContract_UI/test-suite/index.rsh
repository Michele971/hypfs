'reach 0.1';
'use strict';

// This is only for check the Algorand testnet performances. Not use this backend in production!
const REWARD_FOR_PROVER = 10000//send by VERIFIER
const SMART_CONTRACT_MAX_USER = 3

export const main = Reach.App(() => {
    const Creator = Participant('Creator',{ 
    ...hasConsoleLogger,
    position: Bytes(128),
    decentralized_identifier: UInt,
    proof_reveived: Bytes(128),
    reportPosition: Fun([UInt, Maybe(Bytes(128))], Null),
    reportVerification: Fun([UInt, Address], Null),

  });

  const attacherAPI = API('attacherAPI',{
    insert_position: Fun([Bytes(128),UInt], UInt), //PositionAndProof - DID - ReturnField
  });



  const views = View('views', { 
    getCtcBalance: UInt, // Allow users to check the balance of the contract
    getReward: UInt, // Allow the users and verifier to get the reward

  });

 
  setOptions({untrustworthyMaps: true});
  init();

  Creator.publish() //we need that to use the MAP below
  const easy_map = new Map(Bytes(128));
  
  commit();
  Creator.only(() => { 
    const proof_and_position = declassify(interact.position);
    const decentralized_identifier_creator = declassify(interact.decentralized_identifier);
  });

  Creator.publish(proof_and_position, decentralized_identifier_creator); //TODO: add the proof_received

  easy_map[this] = proof_and_position; //setting the first value of the map with Creator values

  commit();
  Creator.publish();

  //logging a message with the DID inserted and the data passed (e.g. proof and position)
  Creator.only(() => interact.reportPosition(decentralized_identifier_creator, easy_map[this]));
  
  // ************ INSERT POSITION API **************
  // the API terminated whe it reaches 3 users
  //the attacher can insert their positions
  const counter = 
  parallelReduce(SMART_CONTRACT_MAX_USER) 
    .invariant(balance() == balance()) // invariant: the condition inside must be true for the all time that the while goes on
    //.define(() => {views.retrieve_results.set(did_user);}) // define: the code inside is executed when a function in the while is called (ex. the api call)
    .while(counter > 0)
    .api(attacherAPI.insert_position, // the name of the api that is called 
      (pos, did, y) => { // the code to execute and the returning variable of the api (y)
        y(counter); //allow the frontend to retrieve the space available 

        easy_map[this] = fromSome(easy_map[this],pos);

        Creator.only(() => interact.reportPosition(did, easy_map[this]));

        return counter - 1; // the returning of the API for the parallel reduce necessary to update the initial variable 
      }
    )
    // TIMEOUT WORKS ONLY ON TESTNET
    // .timeout(relativeTime(deadline), () => { // timeout: function that executes code every amount of time decided by the first parameter
    //   Creator.interact.log("The campaign has finished") // log on the Creator cli to inform the end of the campaign
    //   Anybody.publish(); // publish needed to finish the parallel reduce
    //   return [total_balance,false]; // set keepGoing to false to finish the campaign
    // }); 
    views.getCtcBalance.set(balance());
    views.getReward.set(REWARD_FOR_PROVER);
    commit();
    Creator.publish();



  //for TESTING
  transfer(balance()).to(Creator);
  
  commit();
  

  exit();
});
