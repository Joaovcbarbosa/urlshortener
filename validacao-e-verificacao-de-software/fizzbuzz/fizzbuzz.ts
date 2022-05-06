export function fizzBuzz (n: number): string {  
  if (isDivisibleBy(3, n) && isDivisibleBy(5, n)) return 'fizzbuzz'
  if (isDivisibleBy(3, n)) return 'fizz'
  if (isDivisibleBy(5, n)) return 'buzz'
  return n.toString()
}

function isDivisibleBy(divisor: number, dividend: number): boolean {
  return dividend % divisor === 0
}

export function play (inputArray: number[]): string{
 
  let fizzBuzzArray = inputArray.map((element) =>{
    return fizzBuzz(element);
  }).join(', ')

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