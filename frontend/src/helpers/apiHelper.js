import { v4 as uuidv4 } from 'uuid';

export const getNotebooks = async (userId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebooks?userId=${userId}`
  );

  const asJson = await response.json();

  return asJson;
};

export const getNotebookInfo = async (notebookId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebookInfo?notebookId=${notebookId}`
  );

  const asJson = await response.json();

  return asJson;
};

export const getNotebook = async (notebookId, start, take, sort, tags) => {

  const startSuffix = start ? `&start=${start}` : ''
  const takeSuffix = take ? `&take=${take}` : ''
  const sortSuffix = sort ? `&sort=${sort}` : ''
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebook?notebookId=${notebookId}${startSuffix}${takeSuffix}${sortSuffix}&tags=${tags ?? ''}`
  );

  const asJson = await response.json();
  return asJson;
};

export const getSnippet = async (notebookId, snippetId, userId) => {
  const response = await fetch(
    `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getSnippet?notebookId=${notebookId}&snippetId=${snippetId}&userId=${userId}`
  );

  const asJson = await response.json();

  return asJson;
};

export const newSnippet = async (
  title,
  body,
  tags,
  notebookId,
  userId,
  snippetId = undefined
) => {
  const post = {
    title,
    body,
    tags,
    notebookId,
    userId,
    snippetId: snippetId ?? uuidv4().replaceAll('-', ''),
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
    return data;
  } catch (error) {
    console.log('error', error);
    return null;
  }
};

export const updateSnippet = async (
  title,
  body,
  tags,
  notebookId,
  userId,
  snippetId,
  isStarred,
) => {
  const post = {
    title,
    body,
    tags,
    notebookId,
    userId,
    snippetId,
    isStarred,
  };

  const raw = JSON.stringify(post);

  const requestOptions = {
    method: 'PUT',
    body: raw,
  };

  try {
    const response = await fetch(
      'https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/updateSnippet',
      requestOptions
    );
    const data = await response.text();
    return data;
  } catch (error) {
    console.log('error', error);
    return null;
  }
};

export const deleteSnippet = async (notebookId, userId, snippetId) => {
  const requestOptions = {
    method: 'DELETE',
  };

  try {
    const response = await fetch(
      `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/deleteSnippet?notebookId=${notebookId}&userId=${userId}&snippetId=${snippetId}`,
      requestOptions
    );
    const data = await response.text();
    return data;
  } catch (error) {
    console.log('error', error);
    return null;
  }
};

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
    return data;
  } catch (error) {
    console.log('error', error);
    return null;
  }
};

export const updateNotebook = async (notebookId, name) => {
  const post = {
    name,
    notebookId,
  };

  const raw = JSON.stringify(post);

  const requestOptions = {
    method: 'PUT',
    body: raw,
  };

  try {
    const response = await fetch(
      'https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/updateNotebook',
      requestOptions
    );
    const data = await response.text();
    return data;
  } catch (error) {
    console.log('error', error);
    return null;
  }
};
