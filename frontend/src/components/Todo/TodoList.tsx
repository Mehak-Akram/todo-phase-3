import { Todo } from '../../types';
import TodoItem from './TodoItem';
import EmptyState from '../UI/EmptyState';

interface TodoListProps {
  todos: Todo[] | null | undefined; // Can be null or undefined during loading
  onUpdateTodo: (id: string, content: string) => void;
  onToggleTodo: (id: string, completed: boolean) => void;
  onDeleteTodo: (id: string) => void;
}

export default function TodoList({ todos, onUpdateTodo, onToggleTodo, onDeleteTodo }: TodoListProps) {
  // Ensure todos is an array before trying to map over it
  const todosArray = Array.isArray(todos) ? todos : [];

  if (todosArray.length === 0) {
    return (
      <EmptyState
        title="No todos yet"
        message="Get started by adding a new todo above."
        icon={
          <svg
            className="w-16 h-16 mx-auto text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        }
      />
    );
  }

  return (
    <div className="space-y-3">
      {todosArray.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onUpdate={onUpdateTodo}
          onToggle={onToggleTodo}
          onDelete={onDeleteTodo}
        />
      ))}
    </div>
  );
}