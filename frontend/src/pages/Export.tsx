import { Card, CardContent } from "../components/ui/card";

export default function Export() {
  return (
    <Card>
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Export Data</h2>
        <p className="text-gray-700">Choose your export options for signals and results.</p>
      </CardContent>
    </Card>
  );
}