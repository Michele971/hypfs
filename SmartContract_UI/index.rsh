'reach 0.1';
'use strict';
//NOTE:
// TODO: This smart contract is empower to validate if the positions of user are correct
// There is a smart contract for every different position
// TODO: The Smart Contract will expire after a specific amount of time


const commonInteract = {
  ...hasConsoleLogger,
  position: Bytes(128),
  decentralized_identifier: Bytes(128),
  proof_reveived: Bytes(128),
  reportPosition: Fun([Bytes(128), Maybe(Bytes(128))], Null)
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
    insert_position: Fun([Bytes(128),Bytes(128)], Bytes(128)),
    //insert_did: Fun([Bytes(128)], Null),
    //insert_proof: Fun([Bytes(128)], Null),
  });


  setOptions({untrustworthyMaps: true});
  init();

  Creator.publish() //we need that to use the MAP below
  const easy_map = new Map(Bytes(128),Bytes(128));
  commit();
  Creator.only(() => { 
    const proof_and_position = declassify(interact.position);
    const decentralized_identifier_creator = declassify(interact.decentralized_identifier);
  });

  Creator.publish(proof_and_position, decentralized_identifier_creator); //TODO: add the proof_reveived
  easy_map[decentralized_identifier_creator] = fromSome(easy_map[decentralized_identifier_creator], proof_and_position);
  //only for DEBUG
  each([Creator, A], () => interact.reportPosition(decentralized_identifier_creator, easy_map[decentralized_identifier_creator]));

  commit();
  
  Creator.publish();
  Creator.interact.log("Before parallel reduce")
  //the attacher can insert their positions
  const keepGoing = 
  parallelReduce(true) 
    .invariant(balance() == balance()) // invariant: the condition inside must be true for the all time that the while goes on
    //.define(() => {views.getCtcBalanceV.set(balance());}) // define: the code inside is executed when a function in the while is called (ex. the api call)
    .while(keepGoing)
    .api(attacherAPI.insert_position, // the name of the api that is called 
      // (position_of_attacher) => { // the assume that have to be true to continue the execution of the API
      //   assume(balance()==balance(), 'Not allow to invest more positions ')
      // },      
      //(invst) => invst, // the payment that the users have to do when call the api
      (pos, did, y) => { // the code to execute and the returning variable of the api (y)
        y(pos);
      
        easy_map[did] = fromSome(easy_map[did], pos); // saving the POSITION into the Map 
        Creator.interact.log("somebody added a new position to the map")
        each([Creator, A], () => interact.reportPosition(did, easy_map[did]));
        return true; // the returning of the API for the parallel reduce necessary to update the initial variable 
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