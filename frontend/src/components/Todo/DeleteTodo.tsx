import { useState } from 'react';

interface DeleteTodoProps {
  onDelete: () => void;
  todoContent: string;
}

export default function DeleteTodo({ onDelete, todoContent }: DeleteTodoProps) {
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleDelete = () => {
    onDelete();
    setShowConfirmation(false);
  };

  return (
    <div className="relative">
      {showConfirmation ? (
        <div className="absolute right-0 z-10 p-4 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl shadow-lg min-w-[200px]">
          <p className="text-sm text-white/80 mb-3">
            Delete "{todoContent}"?
          </p>
          <div className="flex space-x-2">
            <button
              onClick={handleDelete}
              className="px-3 py-1.5 text-sm font-medium text-white bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-300 shadow-md"
            >
              Yes
            </button>
            <button
              onClick={() => setShowConfirmation(false)}
              className="px-3 py-1.5 text-sm font-medium text-white/90 bg-white/10 rounded-md hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30 focus:ring-offset-2 transition-colors duration-200 border border-white/20"
            >
              No
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setShowConfirmation(true)}
          className="px-3 py-1.5 text-sm font-medium text-white/90 bg-white/10 rounded-md hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30 focus:ring-offset-2 transition-colors duration-200 border border-white/20"
        >
          Delete
        </button>
      )}
    </div>
  );
}