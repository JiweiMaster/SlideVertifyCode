import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options



# 该函数用来解决拖动二维码的验证问题
def drag_btn(distance,chromeDriver):
    # 拖动按钮的div
    dragBtn = chromeDriver.find_element_by_id("tcaptcha_drag_button")
    ActionChains(chromeDriver).move_to_element(dragBtn).perform()
    ActionChains(chromeDriver).click_and_hold(dragBtn).perform()
    while distance > 5:
        ActionChains(chromeDriver).move_by_offset(5, 0).perform()
        time.sleep(10 / 1000)
        distance -= 5
    ActionChains(chromeDriver).release().perform()

#设置chrome无界面
chrome_options = Options()
chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(chrome_options = chrome_options)
driver = webdriver.Chrome()

wait = ui.WebDriverWait(driver,20)
driver.get("http://www.sf-express.com/cn/sc/dynamic_function/waybill/#search/bill-number/290449890726")
wait.until(lambda  driver: driver.find_element_by_id("tcaptcha_popup"))

#iFrame的div，顺丰的官网是将二维码放置在IFrame里面的，解决了不在一个界面里面的跨域问题
iFrame = driver.find_element_by_id("tcaptcha_popup")
driver.switch_to.frame("tcaptcha_popup")

#开始移动
#这个距离是随便设定的，看实际的调试结果
# distance = 230
# while distance>5:
#     ActionChains(driver).move_by_offset(5, 0).perform()
#     time.sleep(10 / 1000)
#     distance -= 5
# ActionChains(driver).release().perform()

drag_distance = 230
drag_btn(drag_distance,driver)
# 通过下面这个循环基本可以将二维码给解决掉
while True:
    time.sleep(1)
    wait.until(lambda driver: driver.find_element_by_id("tcaptcha_note"))
    return_msg = str(driver.find_element_by_id("tcaptcha_note").text)
    print(return_msg)
    if (return_msg == ""):
        print("success")
        break
    else:
        print("failed")
        if (return_msg == "请控制拼图块对齐缺口"):
            if (drag_distance == 230):
                drag_distance = 245
            elif(drag_distance == 245):
                drag_distance = 215
            elif(drag_distance == 215):
                drag_distance = 230
            else:
                drag_distance = 230
            print("再来一次=>"+str(drag_distance))
            drag_btn(drag_distance, driver)
        if (return_msg == "这题有点难呢，已为您更换题目"):
            drag_distance = 230
            drag_btn(drag_distance, driver)

wait.until(lambda driver: driver.find_element_by_class_name("route-list"))
router_list_text = driver.find_element_by_class_name("route-list").text
print("打印物流信息=>\n")
print(router_list_text)

driver.quit()
#在iframe里面弹出一个popwindow:tcaptcha_popup
#在popwindow里面有一个按钮 ：tcaptcha_drag_button


