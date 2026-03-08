import React from 'react';

function DataTable({ columns, rows }) {
  if (!rows || rows.length === 0) {
    return <p>No data available.</p>;
  }

  const cols = columns || Object.keys(rows[0]);

  return (
    <table>
      <thead>
        <tr>
          {cols.map((col) => (
            <th key={col}>{col}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            {cols.map((col) => (
              <td key={col}>{String(row[col] ?? '')}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DataTable;
