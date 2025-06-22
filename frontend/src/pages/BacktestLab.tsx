import { Card, CardContent } from "../components/ui/card";

export default function BacktestLab() {
  return (
    <Card>
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Backtest Lab</h2>
        <p className="text-gray-700">Test historical performance of your strategies here.</p>
      </CardContent>
    </Card>
  );
}