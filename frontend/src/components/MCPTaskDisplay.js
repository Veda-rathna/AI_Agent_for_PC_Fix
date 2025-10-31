import React, { useState } from 'react';
import './MCPTaskDisplay.css';

const MCPTaskDisplay = ({ mcpExecution }) => {
  const [expandedTasks, setExpandedTasks] = useState({});

  if (!mcpExecution || !mcpExecution.executed || !mcpExecution.tasks) {
    return null;
  }

  const toggleTask = (taskNumber) => {
    setExpandedTasks(prev => ({
      ...prev,
      [taskNumber]: !prev[taskNumber]
    }));
  };

  const { tasks, tasks_completed, tasks_failed, total_tasks } = mcpExecution;

  return (
    <div className="mcp-task-display">
      <div className="mcp-header">
        <h3>Diagnostic Tasks Executed</h3>
        <div className="mcp-stats">
          <span className="stat-item success">
            <span className="stat-label">Completed:</span>
            <span className="stat-value">{tasks_completed}</span>
          </span>
          {tasks_failed > 0 && (
            <span className="stat-item failed">
              <span className="stat-label">Failed:</span>
              <span className="stat-value">{tasks_failed}</span>
            </span>
          )}
          <span className="stat-item total">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{total_tasks}</span>
          </span>
        </div>
      </div>

      <div className="mcp-tasks-list">
        {tasks.map((task, index) => (
          <div 
            key={index} 
            className={`mcp-task-item ${task.success ? 'success' : 'failed'} ${expandedTasks[task.task_number] ? 'expanded' : ''}`}
          >
            <div 
              className="task-header"
              onClick={() => toggleTask(task.task_number)}
            >
              <div className="task-title">
                <span className="task-number">#{task.task_number}</span>
                <span className="task-status">{task.success ? '[OK]' : '[FAIL]'}</span>
                <span className="task-name">{task.task_name}</span>
              </div>
              <div className="task-toggle">
                {expandedTasks[task.task_number] ? '▼' : '▶'}
              </div>
            </div>

            {expandedTasks[task.task_number] && (
              <div className="task-details">
                {task.analysis && (
                  <div className="task-section">
                    <div className="section-label">Analysis:</div>
                    <div className="section-content">{task.analysis}</div>
                  </div>
                )}

                {task.recommendation && (
                  <div className="task-section">
                    <div className="section-label">Recommendation:</div>
                    <div className="section-content recommendation">
                      {task.recommendation}
                    </div>
                  </div>
                )}

                {task.error && (
                  <div className="task-section error">
                    <div className="section-label">Error:</div>
                    <div className="section-content">{task.error}</div>
                  </div>
                )}

                {task.details && Object.keys(task.details).length > 0 && (
                  <div className="task-section">
                    <div className="section-label">Details:</div>
                    <div className="section-content details">
                      <pre>{JSON.stringify(task.details, null, 2)}</pre>
                    </div>
                  </div>
                )}

                {task.timestamp && (
                  <div className="task-timestamp">
                    <small>Executed: {new Date(task.timestamp).toLocaleString()}</small>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {mcpExecution.execution_summary && (
        <details className="mcp-summary">
          <summary>View Full Execution Summary</summary>
          <pre>{mcpExecution.execution_summary}</pre>
        </details>
      )}
    </div>
  );
};

export default MCPTaskDisplay;
