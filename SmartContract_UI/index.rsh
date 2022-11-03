'reach 0.1';
'use strict';

const REWARD_FOR_PROVER = 1000000000000000000/1000//send by VERIFIER. We have 1 ETH / 1000 which is =  0.001
const SMART_CONTRACT_MAX_USER = 4
//NOTES:
// TODO: Maybe using an unique password (for more verifiers) for memory reason

export const main = Reach.App(() => {
    const Creator = Participant('Creator',{ 
    ...hasConsoleLogger,
    position: Bytes(128),
    did: UInt,
    data_inserted: Bytes(512),
    reportPosition: Fun([UInt, Maybe(Bytes(512))], Null),
    reportVerification: Fun([UInt, Address], Null),
    issueDuringVerification: Fun([UInt], Null),

  });

  const attacherAPI = API('attacherAPI',{
    insert_position: Fun([Bytes(512),UInt], UInt), //PositionAndProof - DID - ReturnField
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


  Creator.only(() => { 
    const proof_and_position = declassify(interact.position);
    const decentralized_identifier_creator = declassify(interact.did);
    const data_ins = declassify(interact.data_inserted);
  });

  Creator.publish(proof_and_position, decentralized_identifier_creator, data_ins); //TODO: add the proof_received
  const easy_map = new Map(UInt,Bytes(512));
  easy_map[decentralized_identifier_creator] = data_ins; //setting the first value of the map with Creator values

  commit();
  Creator.publish();

  //logging a message with the DID inserted and the data passed (e.g. proof and position)
  Creator.only(() => interact.reportPosition(decentralized_identifier_creator, easy_map[decentralized_identifier_creator]));
  
  // ************ INSERT POSITION API **************
  // the API terminated whe it reaches 3 users
  //the attacher can insert their positions
  const counter = 
  parallelReduce(SMART_CONTRACT_MAX_USER-1) 
    .invariant(balance() == balance()) // invariant: the condition inside must be true for the all time that the while goes on
    //.define(() => {views.retrieve_results.set(did_user);}) // define: the code inside is executed when a function in the while is called (ex. the api call)
    .while(counter > 0)
    .api(attacherAPI.insert_position, // the name of the api that is called 
      (pos, did, y) => { // the code to execute and the returning variable of the api (y)
        y(counter); //allow the frontend to retrieve the space available 
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

    const keepGoing2_counter = 
    parallelReduce(SMART_CONTRACT_MAX_USER) 
      .invariant(balance() == balance())
      .define(() => {views.getCtcBalance.set(balance());})
      .while(keepGoing2_counter > 0) 
      .api(verifierAPI.insert_money,
        (money) => { // the assume that have to be true to continue the execution of the API
          assume(money > 0);
        },      
        (money) => money, // the payment that the users have to do when call the api
        (money, y) => { 
          y(money);
        
          return keepGoing2_counter;
        }
      )
      .api(verifierAPI.verify, 
        (did, walletAddress, ret) => { 
          // transfer some money to the Prover (attacher)
          if (balance()>=REWARD_FOR_PROVER){
            transfer(REWARD_FOR_PROVER).to(walletAddress); 
            Creator.only(() => interact.reportVerification(did, this));
            delete easy_map[did]; //vector[0] is the did
            ret(walletAddress);
            return keepGoing2_counter -1; 
       
          }else{
            Creator.only(() => interact.issueDuringVerification(did));
            ret(walletAddress);
            return keepGoing2_counter -1; //replace with "keepGoing2_counter -1" during the testing 
          }
        

        }
      )
      .timeout(relativeTime(700/5), () => { // timeout: function that executes code every amount of time decided by the first parameter
        Anybody.publish(); // publish needed to finish the parallel reduce
        return keepGoing2_counter; // set keepGoing to false to finish the campaign
      }); 


  // TODO: the first received position has to be stored in a data structure, will be compared to the subsquent received positions

  transfer(balance()).to(Creator);
  
  commit();
  

  exit();
});
