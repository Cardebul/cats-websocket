import React from "react";



export const ChatList = ({ users, onUserClick }) => {
  return (
    <ul>
      <li>
        <button text="Общий чат" onClick={() => onUserClick(0)}>Общий чат</button>
      </li>
      {users.map((user) => (
        <li key={user.id}>
          <button text={user.username} onClick={() => onUserClick(user.id)}>{user.username}</button>
        </li>
      ))}
    </ul>
  );
};