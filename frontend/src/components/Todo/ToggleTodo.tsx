interface ToggleTodoProps {
  completed: boolean;
  onToggle: (completed: boolean) => void;
}

export default function ToggleTodo({ completed, onToggle }: ToggleTodoProps) {
  return (
    <input
      type="checkbox"
      checked={completed}
      onChange={() => onToggle(!completed)}
      className="w-5 h-5 text-blue-500 rounded focus:ring-blue-400 bg-white/20 border-white/40"
    />
  );
}