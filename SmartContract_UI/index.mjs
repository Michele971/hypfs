import { loadStdlib } from '@reach-sh/stdlib';
import * as backend from './build/index.main.mjs';
import { ask } from '@reach-sh/stdlib';


const stdlib = loadStdlib(process.env);

//setting the user role
let role = "creator" //default
const user_know_id = await ask.ask(`Do you already have a contract id?`, ask.yesno);
if (user_know_id){
  role = "attacher"
}


console.log(`Your role is ${role}`);

const iBalance = stdlib.parseCurrency(1000);
const acc = await stdlib.newTestAccount(iBalance);

console.log(`The consensus network is ${stdlib.connector}.`);
const commonInteract = {
  reportPosition: (position) => console.log(`The first position inserted is: "${position}"`),
};

// CREATOR
if (role === 'creator') {
  const creatorInteract = {
    ...commonInteract,
    position: await ask.ask('Enter your position:', (positionInserted) => {
      let pos_result = !positionInserted ? '44.2834757,11.398155' : positionInserted;
      if (!positionInserted) { console.log(pos_result); }
      return pos_result;
    }),
  };
  const acc = await stdlib.newTestAccount(iBalance);
  // await showBalance(acc);
  const ctc = acc.contract(backend);
  await ctc.participants.Creator(creatorInteract);
  console.log(`Contract info: ${JSON.stringify(await ctc.getInfo())}`);

  // ATTACHER
} else {
  const attacherInteract = {
    ...commonInteract,
  };

  //TODO: send a proof 
  console.log("A smart contract associated to this position already existed.");
  console.log("Please insert the credential of 3 users near to you AND your credential");
  console.log("SIMULATION MODE: the credential is the DID (Decentralized IDentifier)");
  //TODO: design a for that waits for 3 different credential


  const acc = await stdlib.newTestAccount(iBalance);
  const info = await ask.ask('Paste contract info:', (s) => JSON.parse(s));
  const ctc = acc.contract(backend, info);
  await ctc.p.Attacher(attacherInteract);


};
