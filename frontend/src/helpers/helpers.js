export const removeElement = (arr, element) => {
  for(var i = 0; i < arr.length; i++) {
    if(arr[i] === element) {
      arr.splice(i, 1)
      break
    }
  }

  return arr
}
