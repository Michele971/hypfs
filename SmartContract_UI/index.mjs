import { loadStdlib } from '@reach-sh/stdlib';
import * as backend from './build/index.main.mjs';
import { ask } from '@reach-sh/stdlib';
import { done } from '@reach-sh/stdlib/ask.mjs';

let ctc = null;
const stdlib = loadStdlib(process.env);

//setting the user role
let role = "creator" //default
const user_know_id = await ask.ask(`Do you already have a contract id?`, ask.yesno);
if (user_know_id){
  role = "attacher"
}

//setting the call for reach api
const call = async (f) => {
  let res = undefined;
  try {
    res = await f();
    console.log(`res`, res);
    return res;
  } catch (e) {
    res = [`err`, e]
    console.log(`res`, res);
    return false;
  }
};

console.log(`Your role is ${role}`);

const iBalance = stdlib.parseCurrency(1000);
const acc = await stdlib.newTestAccount(iBalance);

console.log(`The consensus network is ${stdlib.connector}.`);
const commonInteract = {
  reportPosition: (did,  proof_and_position) => console.log(`New position inserted \n DID: "${did}" \n proof_and_position: "${proof_and_position}"`),
};

//implement the functions to log inside the backend
commonInteract.log = async (...args) => {
  console.log(...args)
};
// CREATOR
if (role === 'creator') {
  const creatorInteract = {
    ...commonInteract,
    decentralized_identifier: await ask.ask('Enter your DID:', (did_inserted) => {
      return did_inserted;
    }),
    proof_reveived: await ask.ask('Enter the proof:', (proof_inserted) => {
      return proof_inserted; 
    }),
    position: await ask.ask('Enter your position:', (positionInserted) => {
      let pos_result = !positionInserted ? '44.2834757,11.398155' : positionInserted;
      if (!positionInserted) { console.log(pos_result); }
      return pos_result;
    }),
  };
  const acc = await stdlib.newTestAccount(iBalance);
  // await showBalance(acc);
  //const ctc = acc.contract(backend); //OLD VERSION
  ctc = acc.contract(backend); //creating the contract
  ctc.getInfo().then((info) => {
    console.log(`The contract is deployed as = ${JSON.stringify(info)}`); //display the id of the contract. It was "parse" not "stringify"
  });
  //console.log(`Contract info: ${JSON.stringify(await ctc.getInfo())}`);


  //await ctc.participants.Creator(creatorInteract); //OLD VERSION


  console.log("The POSITION is ",creatorInteract.position); //for testing

  const part = backend.Creator;
  await part(ctc, creatorInteract); 
  // ATTACHER
} else {
  const attacherInteract = {
    ...commonInteract,
  };

  //TODO: receive the proofs
  console.log("A smart contract associated to this position already existed.");
  console.log("SIMULATION MODE: the credential is the DID (Decentralized IDentifier)");
  //TODO: design the interaction with VERIFIERS


  const acc = await stdlib.newTestAccount(iBalance);
  const info = await ask.ask(
    `Please paste the contract information:`,
    JSON.parse
  );

  ctc = acc.contract(backend, info);
  
  var did = await ask.ask(
    `What is your DID?`,
    (did => did)
  );
  var location_attacher = await ask.ask(
    `What is your Location?`,
    (x => x)
  );
  var proof_attacher = await ask.ask(
    `What is your Proof?`,
    (proof_attacher => proof_attacher)
  );

  //Proof + Location, e.g "jshsj2a9sjdja3ksl-G294A02"
  var proof_and_location = String(proof_attacher)+"-"+String(location_attacher)
  const attacher_api = ctc.a.attacherAPI;
  
  await call(() => attacher_api.insert_position(
        String(proof_and_location),
        String(did)
      )
    );



};


done();