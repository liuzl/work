public class Main {
	public static void main(String[] args) throws Exception {
		Earley.Rule N = new Earley.Rule("N", new Earley.Production("time"), new Earley.Production("航班"), new Earley.Production("香蕉"), 
				new Earley.Production("flies"), new Earley.Production("男孩"), new Earley.Production("望远镜"));
		Earley.Rule D = new Earley.Rule("D", new Earley.Production("the"), new Earley.Production("一个"), new Earley.Production("an"));
		Earley.Rule V = new Earley.Rule("V", new Earley.Production("book"), new Earley.Production("吃了"), new Earley.Production("sleep"), 
				new Earley.Production("saw"), new Earley.Production("认为"));
		Earley.Rule P = new Earley.Rule("P", new Earley.Production("with"), new Earley.Production("in"), new Earley.Production("on"), 
				new Earley.Production("at"), new Earley.Production("through"));
		Earley.Rule C = new Earley.Rule("C", new Earley.Production("that"));

		Earley.Rule PP = new Earley.Rule("PP");
		Earley.Rule NP = new Earley.Rule("NP", new Earley.Production(D, N), new Earley.Production("约翰"), new Earley.Production("比尔"),
				new Earley.Production("houston"));
		NP.add(new Earley.Production(NP, PP));
		PP.add(new Earley.Production(P, NP));

		Earley.Rule VP = new Earley.Rule("VP", new Earley.Production(V, NP));
		VP.add(new Earley.Production(VP, PP));
		Earley.Rule S = new Earley.Rule("S", new Earley.Production(NP, VP), new Earley.Production(VP));
		Earley.Rule Sbar = new Earley.Rule("S'", new Earley.Production(C, S));
		VP.add(new Earley.Production(V, Sbar));

		// let's parse some sentences!
		for (String text : new String[] {"约翰 吃了 一个 香蕉", "book the 航班 through houston", 
			"约翰 saw the 男孩 with the 望远镜", "约翰 认为 that 比尔 吃了 一个 香蕉"}) {
			Earley.Parser p = new Earley.Parser(S, text);
			System.out.printf("Parse trees for '%s'\n", text);
			System.out.println("===================================================");
			for (Earley.Node<Earley.TableState> tree : p.getTrees()) {
				tree.print(System.out);
				System.out.println();
			}
		}
	}
}
