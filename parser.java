import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Scanner;

public class parser {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder inputBuilder = new StringBuilder();

        while (sc.hasNextLine()) {
            inputBuilder.append(sc.nextLine());
        }

        String inputJson = inputBuilder.toString();
        JSONArray tokens = new JSONArray(inputJson);

        // Very naive check: just make sure first 5 tokens match a simple pattern
        if (tokens.length() >= 5 &&
            tokens.getJSONObject(0).getString("type").equals("KEYWORD") &&
            tokens.getJSONObject(1).getString("type").equals("IDENTIFIER") &&
            tokens.getJSONObject(2).getString("type").equals("OPERATOR") &&
            tokens.getJSONObject(3).getString("type").equals("NUMBER") &&
            tokens.getJSONObject(4).getString("type").equals("SYMBOL")) {

            JSONObject tree = new JSONObject();
            tree.put("type", "Assignment");
            JSONArray children = new JSONArray();

            children.put(new JSONObject().put("type", "Type").put("value", tokens.getJSONObject(0).getString("value")));
            children.put(new JSONObject().put("type", "Identifier").put("value", tokens.getJSONObject(1).getString("value")));
            children.put(new JSONObject().put("type", "Operator").put("value", tokens.getJSONObject(2).getString("value")));
            children.put(new JSONObject().put("type", "Number").put("value", tokens.getJSONObject(3).getString("value")));
            children.put(new JSONObject().put("type", "Semicolon").put("value", tokens.getJSONObject(4).getString("value")));

            tree.put("children", children);
            System.out.println(tree.toString(2));
        } else {
            System.out.println("{\"error\": \"Syntax error: Expected assignment statement\"}");
        }

        sc.close();
    }
}
