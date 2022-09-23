'reach 0.1';
'use strict';

const REWARD_FOR_PROVER = 100000000000000000//send by VERIFIER
const SMART_CONTRACT_MAX_USER = 3
//NOTES:
// TODO: This smart contract is empower to validate if the positions of users are correct
// There is a smart contract for every different position
// TODO: The Smart Contract will expire after a specific amount of time
// TODO: Add the geofence attribute to the smart contract (radius, etc etc ....). In this way 
//       we can design more checks such as: the position received must be inside the geofence area.
// TODO: The smart contract will know the verifier (?) ----> still to be decided. 
//       Maybe using an unique password (for more verifiers) for memory reason
// TODO: check that the proofs inserted unique and not already present
// TODO: print balance of the contract() using the view
// TODO: print the reward that will be assign to everyone that has a valid proof, after verify it

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

  const verifierAPI = API('verifierAPI',{
    insert_money: Fun([UInt], UInt), 
    verify: Fun([UInt,Address], Address),
  });

  const views = View('views', { 
    getCtcBalance: UInt, // Allow users to check the balance of the contract
    getReward: UInt, // Allow the users and verifier to get the reward

  });

 
  setOptions({untrustworthyMaps: true});
  init();

  Creator.publish() //we need that to use the MAP below
  const easy_map = new Map(UInt,Bytes(128));
  
  commit();
  Creator.only(() => { 
    const proof_and_position = declassify(interact.position);
    const decentralized_identifier_creator = declassify(interact.decentralized_identifier);
  });

  Creator.publish(proof_and_position, decentralized_identifier_creator); //TODO: add the proof_received

  easy_map[decentralized_identifier_creator] = proof_and_position; //setting the first value of the map with Creator values

  commit();
  Creator.publish();

  //logging a message with the DID inserted and the data passed (e.g. proof and position)
  Creator.only(() => interact.reportPosition(decentralized_identifier_creator, easy_map[decentralized_identifier_creator]));
  
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
 
        //TODO: notify the attacher (not the creator) when the key is already used 
        // if(easy_map[did] != Null){ //TODO: FIX THIS CHECK. CHECK if map contain THE ID INSERTED --------------> IMPORTANT
        //   return true; //TODO: THIS HAS TO RETURN TRUE
        // }
        /** 
         * The line below manages the case when the key is already 
         * assigned to a specific value 
         * */
        easy_map[did] = fromSome(easy_map[did],pos);

        Creator.only(() => interact.reportPosition(did, easy_map[did]));

        return counter - 1; // the returning of the API for the parallel reduce necessary to update the initial variable 
      }
    )
    // TIMEOUT WORKS ONLY ON TESTNET
    // .timeout(relativeTime(1260/5), () => { // timeout: function that executes code every amount of time decided by the first parameter
    //   Anybody.publish(); // publish needed to finish the parallel reduce
    //   return counter; // set keepGoing to false to finish the campaign
    // }); 
    views.getCtcBalance.set(balance());
    views.getReward.set(REWARD_FOR_PROVER);
    commit();
    Creator.publish();

    const keepGoing2 = 
    parallelReduce(true) 
      .invariant(balance() == balance())
      .define(() => {views.getCtcBalance.set(balance());})
      .while(keepGoing2)
      .api(verifierAPI.insert_money,
        (money) => { // the assume that have to be true to continue the execution of the API
          assume(money > 0);
        },      
        (money) => money, // the payment that the users have to do when call the api
        (money, y) => { 
          y(money);
        
          return true;
        }
      )
      .api(verifierAPI.verify, 
        (did, walletAddress, ret) => { 
          // transfer some money to the Prover (attacher)
          if (balance()>=REWARD_FOR_PROVER){
            transfer(REWARD_FOR_PROVER).to(walletAddress); //TODO: change amount transfered. THE TRANSFER DOES NOT WORKS.
            Creator.only(() => interact.reportVerification(did, this));
            ret(walletAddress);
          }
          //transfer(balance()).to(walletAddress); //TODO: change amount transfered
          ret(walletAddress);
          delete easy_map[did]; //vector[0] is the did
          // Creator.only(() => interact.reportVerification(did, this));

          
          // print this for debugging
          // Creator.only(() => interact.reportVerification(balance(), this));
          // Creator.only(() => interact.reportVerification(REWARD_FOR_PROVER, this));

          return true; //TODO: THIS HAS TO BE TRUEE, false only for testing
        }
      )
      // .timeout(relativeTime(350/5), () => { // timeout: function that executes code every amount of time decided by the first parameter
      //   Anybody.publish(); // publish needed to finish the parallel reduce
      //   return false; // set keepGoing to false to finish the campaign
      // }); 


  // TODO: the first received position has to be stored in a data structure, will be compared to the subsquent received positions

  //for TESTING
  transfer(balance()).to(Creator);
  
  commit();
  

  exit();
});
