export function fizzBuzz (n: number): string {
  
  if (n % 3 === 0 && n % 5 === 0){
    return 'fizzbuzz'
  }  
  if (n % 3 === 0){
    return 'fizz'
  }
  if (n % 5 === 0){
    return 'buzz'
  }  
  return n.toString()
}

export function play (inputArray: number[]): string[] {
  let fizzBuzzArray = new Array(); 
  inputArray.forEach(function (value) {
    let returnString = fizzBuzz(value)
    fizzBuzzArray.push(returnString)
  }); 
  return fizzBuzzArray
}

function main(){
  let inputArray = new Array(); 
  for(let i = 1; i <= 100; i++)
    inputArray.push(i)
  
  let fizzBuzzArray = play(inputArray)
  console.log(fizzBuzzArray)
}

main()