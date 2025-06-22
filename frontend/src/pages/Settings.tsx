import { Card, CardContent } from "../components/ui/card";

export default function Settings() {
  return (
    <Card>
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Platform Settings</h2>
        <p className="text-gray-700">Control features, upload logo, and manage integrations.</p>
      </CardContent>
    </Card>
  );
}