import { useState } from 'react';
import { Todo } from '../../types';
import ToggleTodo from './ToggleTodo';
import DeleteTodo from './DeleteTodo';
import EditTodo from './EditTodo';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: string, content: string) => void;
  onToggle: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
}

export default function TodoItem({ todo, onUpdate, onToggle, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);

  const handleUpdate = (content: string) => {
    onUpdate(todo.id, content);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  const handleToggle = () => {
    onToggle(todo.id, todo.completed);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <div className={`flex items-center justify-between p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl ${todo.completed ? 'text-white/40' : 'text-white'}`}>
      <div className="flex items-center flex-1">
        <ToggleTodo completed={todo.completed} onToggle={handleToggle} />
        {isEditing ? (
          <EditTodo
            initialContent={todo.content}
            onSave={handleUpdate}
            onCancel={handleCancel}
          />
        ) : (
          <span
            className={`ml-3 flex-1 ${todo.completed ? 'line-through' : ''}`}
            onClick={() => setIsEditing(true)}
          >
            {todo.content}
          </span>
        )}
      </div>

      <div className="flex space-x-2">
        {!isEditing && (
          <>
            <button
              onClick={() => setIsEditing(true)}
              className="px-3 py-1.5 text-sm font-medium text-white/90 bg-white/10 rounded-md hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30 focus:ring-offset-2 transition-colors duration-200 border border-white/20"
            >
              Edit
            </button>
            <DeleteTodo onDelete={handleDelete} todoContent={todo.content} />
          </>
        )}
      </div>
    </div>
  );
}