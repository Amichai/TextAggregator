export const getNotebooks = async (userId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebooks?userId=${userId}`
  )

  const asJson = await response.json()

  return asJson
}

export const getNotebookInfo = async (notebookId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebookInfo?notebookId=${notebookId}`
  )

  const asJson = await response.json()

  return asJson
}

export const getNotebook = async (notebookId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebook?notebookId=${notebookId}`
  )

  const asJson = await response.json()

  return asJson
}

export const newSnippet = async (title, body, tags, notebookId, userId) => {
  const post = {
    title,
    body,
    tags,
    notebookId,
    userId,
  };

  const raw = JSON.stringify(post);

  const requestOptions = {
    method: 'POST',
    body: raw,
  };

  try {
    const response = await fetch(
      'https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/newSnippet',
      requestOptions
    );
    const data = await response.text();
    return data
  } catch (error) {
    console.log('error', error);
    return null;
  }
}

export const newNotebook = async (name, notebookId, userId) => {
  const post = {
    name,
    notebookId,
    userId,
  };

  const raw = JSON.stringify(post);

  const requestOptions = {
    method: 'POST',
    body: raw,
  };

  try {
    const response = await fetch(
      'https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/newNotebook',
      requestOptions
    );
    const data = await response.text();
    return data
  } catch (error) {
    console.log('error', error);
    return null;
  }
}