import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public class Conesize {
	static String workingDir = "C:/Users/Thakur/Desktop/Paper1/";
	static String Filename = "AS_Numbers";
	public static void main(String[] args) throws java.lang.IndexOutOfBoundsException
	{
		try 
		{

			int[] AS = new int [500000];
			int ctr=0;
			BufferedReader br = new BufferedReader(new FileReader(new File(workingDir +Filename+".txt")));

			String strline;int ptr=0;
			String splitted[] = null;
			while((strline = br.readLine()) != null)
			{
				splitted = strline.split(" ");
				AS[ctr++]= Integer.valueOf(splitted[0]);
			}
			br.close();

			File file_sample = new File(workingDir + "/Cone_Size.txt");
			if(!file_sample.exists())
				file_sample.createNewFile();

			for(int i=0;i<AS.length-2;i++)
			{
				BufferedWriter bw_s = new BufferedWriter(new FileWriter(file_sample,true));

				String hatao = String.valueOf(AS[i]);
				if (!hatao.equals("57724") && !hatao.equals("394437") && 
						!hatao.equals("56630")&& !hatao.equals("30823")&&!hatao.equals("394644") 
						&&!hatao.equals("35761")&& !hatao.equals("23304")&& !hatao.equals("64073")
						&& !hatao.equals("16200")&& !hatao.equals("394497")&& !hatao.equals("20559")
						&& !hatao.equals("64049")&& !hatao.equals("5582")&& !hatao.equals("263903")
						&& !hatao.equals("203695")&& !hatao.equals("204152")&& !hatao.equals("263891")
						&& !hatao.equals("204044") && !hatao.equals("203912")&& !hatao.equals("203764"))
				{
					System.out.println("you inside jsoup for "+ String.valueOf(AS[i]));
					Document doc = Jsoup.connect("http://as-rank.caida.org/?mode0=as-info&mode1=as-table&as="+AS[i]).timeout(40*1000).get();
					Elements content = doc.getElementsByTag("tbody");
					Element pre_1= content.get(1);
					Elements rows = pre_1.getElementsByTag("tr");
					Element rnum=rows.get(5);
					Elements con=rnum.getElementsByTag("td");				
					//String text = con.text();
					bw_s.write(AS[i]+" "+con.text());
					bw_s.newLine();
				}
				bw_s.close();
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}

}