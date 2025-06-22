import { Card, CardContent } from "../components/ui/card";

export default function Performance() {
  return (
    <Card>
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Performance Dashboard</h2>
        <p className="text-gray-700">Visualize and monitor performance over time.</p>
      </CardContent>
    </Card>
  );
}