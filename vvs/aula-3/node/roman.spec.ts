import { toRoman } from './roman'

describe('integer to roman numeral converter', () => {
  test('should return I for 1', () => {
    expect(toRoman(1)).toEqual('I')
  })
  test('should return IV for 4', () => {
      expect(toRoman(4)).toEqual('IV')
    })
  test('should return V for 5', () => {
      expect(toRoman(5)).toEqual('V')
    })
  test('should return X for 10', () => {
      expect(toRoman(1)).toEqual('I')
    })
  test('should return L for 50', () => {
      expect(toRoman(50)).toEqual('L')
    })
  test('should return XL for 40', () => {
      expect(toRoman(40)).toEqual('XL')
    })
  test('should return XXXIII for 33', () => {
      expect(toRoman(33)).toEqual('XXXIII')
    })
  test('should return C for 100', () => {
      expect(toRoman(100)).toEqual('C')
    })
  test('should return CLXXVIII for 178', () => {
      expect(toRoman(178)).toEqual('CLXXVIII')
    })
  test('should throw error for negative numbers', () => {
      expect(() =>{
        toRoman(-1)
      }).toThrow(new RangeError('Number out of range for Roman numerals.'))
    })  
})