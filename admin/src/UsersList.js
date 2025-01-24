import React, { useEffect, useState } from 'react';

const UsersList = () => {
  const [users, setUsers] = useState([]);

  // Define fetchData function
  const fetchData = () => {
    fetch('http://127.0.0.1:5000/api/users')
      .then((response) => response.json())
      .then((data) => {
        setUsers(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  useEffect(() => {
    fetchData(); // Fetch data immediately
    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Top Players by Total Cost of Objects</h1>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Apple Count</th>
            <th>Banana Count</th>
            <th>Soup Count</th>
            <th>Carrot Count</th>
            <th>Scrooge Coin Count</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.userId}>
              <td>{user.userId}</td>
              <td>{user.objects.find((obj) => obj.name === 'apple')?.count || 0}</td>
              <td>{user.objects.find((obj) => obj.name === 'banana')?.count || 0}</td>
              <td>{user.objects.find((obj) => obj.name === 'soup')?.count || 0}</td>
              <td>{user.objects.find((obj) => obj.name === 'carrot')?.count || 0}</td>
              <td>{user.objects.find((obj) => obj.name === 'Scrooge coin')?.count || 0}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UsersList;