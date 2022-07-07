'reach 0.1';

//NOTE:
// TODO: This smart contract is empower to validate if the positions of user are correct
// There is a smart contract for every different position
// TODO: The Smart Contract will expire after a specific amount of time


const commonInteract = {
  position: Bytes(128),
  reportPosition: Fun([Bytes(128)], Null)
};
const creatorInteract = {
  ...commonInteract,
};
const attacherInteract = {
  ...commonInteract,
};


export const main = Reach.App(() => {
  const C = Participant('Creator', creatorInteract);
  const A = Participant('Attacher', attacherInteract);
  init();

  C.only(() => { 
    const position = declassify(interact.position);
  });
  C.publish(position);
  commit();

  // TODO: the first received position has to be stored in a data structure, will be compared to the subsquent received positions


  each([C, A], () => interact.reportPosition(position));


  exit();
});