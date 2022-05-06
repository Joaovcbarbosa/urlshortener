import { fizzBuzz } from './fizzbuzz'
import { play } from './fizzbuzz'

describe('Function FizzBuzz. Verify the condition of a single integer', () => {
  it('should return the integer if its not divisible by 3 or 5', () => {
    expect(fizzBuzz(1)).toEqual('1')
  })
  it('should return "fizz" if the integer is divisible by 3', () => {
    expect(fizzBuzz(6)).toEqual('fizz')
  })  
  it('should return "buzz" if the integer is divisible by 5', () => {
    expect(fizzBuzz(5)).toEqual('buzz')
  })
  it('should return "fizzbuzz" if the integer is divisible by 3 and 5', () => {
    expect(fizzBuzz(15)).toEqual('fizzbuzz')
  })
})

describe('Function Play. Receive a array of integers and verify one by one', () => {
  it('should return the list of strings without any fizz or buzz', () => {
    expect(play([1, 2])).toEqual('1, 2')
  })
  it('should return the list of strings only with fizz', () => {
    expect(play([3, 6])).toEqual('fizz, fizz')
  })
  it('should return the list of strings only with buzz', () => {
    expect(play([5, 10])).toEqual('buzz, buzz')
  })
  it('should return the list of strings only with "fizzbuzz"', () => {
    expect(play([15, 30])).toEqual('fizzbuzz, fizzbuzz')
  })
  it('should return the list of strings according to the "fizzbuzz" function', () => {
    expect(play([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])).toEqual('1, 2, fizz, 4, buzz, fizz, 7, 8, fizz, buzz, 11, fizz, 13, 14, fizzbuzz')
  })
})