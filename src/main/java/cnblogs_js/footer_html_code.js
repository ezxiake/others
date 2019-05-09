<script language="javascript" type="text/javascript">
// Generate a directory index list
// ref: http://www.cnblogs.com/wangqiguo/p/4355032.html
// ref: https://www.cnblogs.com/xuehaoyue/p/6650533.html
// modified by: keyshaw
function GenerateContentList()
{
    var mainContent = $('#cnblogs_post_body');

    //If your chapter title isn't `h2`, You just replace the h2 here.
    var h2_list = $('#cnblogs_post_body h2');
    // var go_to_bottom = '<div style="text-align: right;"><a href="#_page_bottom" style="color:#f68a33">Go to page bottom</a></div>';
    var bottom_label = '<div style="text-align: right;"><a href="#_labelTop" style="color:#f68a33">Back to the top</a><a name="_page_bottom"></a></div>'

    if(mainContent.length < 1)
        return;

    if(h2_list.length>0)
    {
        var content = '<div style="text-align: right;"><a href="#_page_bottom" style="color:#f68a33">Go to page bottom</a></div><a name="_labelTop"></a>';
        content += '<div id="navCategory" style="color:#152e97;">';
        // coutent += '<div style="text-align: right;"><a href="#_page_bottom" style="color:#f68a33">Go to page bottom</a></div>'
        content += '<h1 style="font-size:16px;background: #f68a33;border-radius: 6px 6px 6px 6px;box-shadow: 0 0 0 1px #5F5A4B, 1px 1px 6px 1px rgba(10, 10, 0, 0.5);color: #FFFFFF;font-size: 17px;font-weight: bold;height: 25px;line-height: 25px;margin: 18px 0 !important;padding: 8px 0 5px 30px;"><b>Catalogue</b></h1>';
        // ol - ordered; ul - unordered
        content += '<ol>';
        for(var i=0; i<h2_list.length; i++)
        {
            // add 'Back to the top' before h2
            var go_to_top_2 = '<div style="text-align: right;"><a href="#_labelTop" style="color:#f68a33">Back to the top</a><a name="_label' + i + '"></a></div>';
            $(h2_list[i]).before(go_to_top_2);
            
            var h3_list = $(h2_list[i]).nextAll("h3");
            
            var li3_content = '';
            for(var j=0; j<h3_list.length; j++)
            {

                var tmp_3 = $(h3_list[j]).prevAll('h2').first();
                if(!tmp_3.is(h2_list[i]))
                    break;

                var go_to_top_3 = '<div style="text-align: right;"><a href="#_labelTop" style="color:#f68a33">Back to the top</a><a name="_label' + i + '_' + j + '"></a></div>';
                $(h3_list[j]).before(go_to_top_3);

                // li3_content += '<li><a href="#_label' + i + '_' + j + '"style="font-size:12px;color:#2b6695;">' + $(h3_list[j]).text() + '</a></li>';

                var li4_content = '';
                var h4_list = $(h3_list[j]).nextAll("h4");
                for(var k=0; k<h4_list.length; k++)
                {
                    var tmp_4 = $(h4_list[k]).prevAll('h3').first();
                    if(!tmp_4.is(h3_list[j]))
                        break;

                    var go_to_top_4 = '<div style="text-align: right;"><a href="#_labelTop" style="color:#f68a33">Back to the top</a><a name="_label' + i + '_' + j + '_' + k + '"></a></div>';
                    $(h4_list[k]).before(go_to_top_4);

                    li4_content += '<li><a href="#_label' + i + '_' + j + '_' + k + '"style="font-size:12px;color:#2b6695;">' + $(h4_list[k]).text() + '</a></li>';
                }

                
                if(li4_content.length > 0)
                    li3_content += '<li><a href="#_label' + i + '_' + j + '"style="font-size:12px;color:#2b6695;">' + $(h3_list[j]).text() + '</a><ul>' + li4_content + '</ul></li>';
                else
                    li3_content += '<li><a href="#_label' + i + '_' + j + '"style="font-size:12px;color:#2b6695;">' + $(h3_list[j]).text() + '</a></li>';

            }

            var li2_content = '';
            if(li3_content.length > 0)
                li2_content = '<li><a href="#_label' + i + '"style="font-size:12px;color:#2b6695;">' + $(h2_list[i]).text() + '</a><ul>' + li3_content + '</ul></li>';
            else
                li2_content = '<li><a href="#_label' + i + '"style="font-size:12px;color:#2b6695;">' + $(h2_list[i]).text() + '</a></li>';
            content += li2_content;

        }
        content += '</ol>';
        content += '</div><p>&nbsp;</p>';
        content += '<hr />';

        // $(mainContent[0]).prepend(go_to_bottom);
        $(mainContent[0]).prepend(content);
        $(mainContent[0]).append(bottom_label);
    }
}

GenerateContentList();
</script>