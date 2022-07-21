'reach 0.1';
'use strict';

const myFromMaybe = (m) => fromMaybe(m, (() => 0), ((x) => x));

//NOTES:
// TODO: This smart contract is empower to validate if the positions if user are correct
// There is a smart contract for every different position
// TODO: The Smart Contract will expire after a specific amount of time
// TODO: Add the geofence attribute to the smart contract (radius, etc etc ....). In this way 
//       we can design more checks such as: the position received must be inside the geofence area.
// TODO: The smart contract will know the verifier (?) ----> still to be decided. 
//       Maybe using an unique password (for more verifiers) for memory reason
// TODO: check that the proofs inserted unique and not already present
//
//
const commonInteract = {
  ...hasConsoleLogger,
  position: Bytes(128),
  decentralized_identifier: UInt,
  proof_reveived: Bytes(128),
  reportPosition: Fun([UInt, Maybe(Bytes(128))], Null),

  //for testing
  report_results: Fun([Bytes(128)], Null)
};
const creatorInteract = {
  ...commonInteract,
};
const attacherInteract = {
  ...commonInteract,
};


export const main = Reach.App(() => {
  const Creator = Participant('Creator', creatorInteract);
  //TODO: remove the Attacher participant and add the Verifier
  const A = Participant('Attacher', attacherInteract); 

  const attacherAPI = API('attacherAPI',{
    insert_position: Fun([Bytes(128),UInt], Bytes(128)), //PositionAndProof - DID - ReturnField
  });

  const verifierAPI = API('verifierAPI',{
    verify: Fun([array], Bool),
  });
 
  const views = View('views', { 
    retrieve_results: Fun([UInt], Bytes(128)), // View that let Verifier checks the retrieve data
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
  //setting the view
  views.retrieve_results.set((m) => fromSome(easy_map[m], proof_and_position));//the default is proof_and_position


  
  
  Creator.interact.log("Before parallel reduce");
  // ************ INSERT POSITION API **************
  //the attacher can insert their positions
  const keepGoing = 
  parallelReduce(true) 
    .invariant(balance() == balance()) // invariant: the condition inside must be true for the all time that the while goes on
    //.define(() => {views.retrieve_results.set(did_user);}) // define: the code inside is executed when a function in the while is called (ex. the api call)
    .while(keepGoing)
    .api(attacherAPI.insert_position, // the name of the api that is called 
      (pos, did, y) => { // the code to execute and the returning variable of the api (y)
        y(pos);
        
        //TODO: notify the attacher (not the creator) when the key is already used 
        if(easy_map[did] != Null){
          Creator.interact.log("The key is already used");
          return true;
        }
        /** 
         * The line below manages the case when the key is already 
         * assigned to a specific value 
         * */
        easy_map[did] = fromSome(easy_map[did],pos);

        Creator.interact.log("Somebody added a new position to the map");
        each([Creator, A], () => interact.reportPosition(did, easy_map[did]));

        return true; // the returning of the API for the parallel reduce necessary to update the initial variable 
      }
    )
    .api(verifierAPI.verify, 
      (vector, y) => { 
        y(vector[0]);

        delete easy_map[vector[0]]; //vector[0] is the did

        return true; 
      }
    )
    // TIMEOUT WORKS ONLY ON TESTNET
    // .timeout(relativeTime(deadline), () => { // timeout: function that executes code every amount of time decided by the first parameter
    //   Creator.interact.log("The campaign has finished") // log on the Creator cli to inform the end of the campaign
    //   Anybody.publish(); // publish needed to finish the parallel reduce
    //   return [total_balance,false]; // set keepGoing to false to finish the campaign
    // }); 
  



  // TODO: the first received position has to be stored in a data structure, will be compared to the subsquent received positions

  //for TESTING
  transfer(balance()).to(Creator);
  
  commit();
  

  exit();
});