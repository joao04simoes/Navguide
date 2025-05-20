function trilaterate(A, da, B, db, C, dc) {

}

const A = { x: 0, y: 3 };
const B = { x: 10, y: 0 };
const C = { x: 5, y: 10 };


const da = 5;
const db = 6;
const dc = 5.4;

const position = trilaterate(A, da, B, db, C, dc);
console.log("Estimated position:", position);
