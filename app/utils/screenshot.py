import os
import time
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def take_full_page_screenshot(url=None, output_filename=None, delay=8, cookies=None, html_content=None):
    """
    Takes a full-page screenshot using Selenium.
    
    Args:
        url (str, optional): The URL to capture. Not used if html_content is provided.
        output_filename (str, optional): Filename for the screenshot. If not provided, 
                                         generates a timestamp-based filename
        delay (int, optional): Seconds to wait for the page to fully load
        cookies (list, optional): List of cookies to add to the browser
        html_content (str, optional): HTML content to render for screenshot instead of URL
    
    Returns:
        dict: Dictionary with success flag and path/error message
    """
    driver = None
    temp_html_file = None
    try:
        # Get the base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(base_dir, 'static', 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Set up Chrome options with SSL error handling
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Use newer headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-file-access-from-files")
        
        # Set up the driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # If HTML content is provided, create a temporary HTML file and open it directly
        if html_content:
            # Create a temporary directory for HTML files if it doesn't exist
            temp_dir = os.path.join(base_dir, 'temp_html')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create a temporary HTML file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_html_file = os.path.join(temp_dir, f"temp_{timestamp}.html")
            
            with open(temp_html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Open the local HTML file
            file_url = f"file:///{temp_html_file.replace(os.sep, '/')}"
            driver.get(file_url)
            
            # Execute JavaScript to check image loading
            try:
                driver.execute_script("""
                    // Function to check if all images are loaded
                    function areAllImagesLoaded() {
                        var imgs = document.getElementsByTagName('img');
                        for (var i = 0; i < imgs.length; i++) {
                            if (!imgs[i].complete) {
                                return false;
                            }
                        }
                        return true;
                    }
                    
                    // Wait for images if not already loaded
                    if (!areAllImagesLoaded()) {
                        var imgPromises = [];
                        var imgs = document.getElementsByTagName('img');
                        
                        for (var i = 0; i < imgs.length; i++) {
                            if (!imgs[i].complete) {
                                imgPromises.push(new Promise(function(resolve) {
                                    imgs[i].onload = resolve;
                                    imgs[i].onerror = resolve; // Handle errors too
                                }));
                            }
                        }
                        
                        Promise.all(imgPromises).then(function() {
                            console.log('All images loaded');
                        });
                    }
                """)
            except Exception as js_error:
                print(f"Warning: JavaScript execution error: {js_error}")
                
        else:
            # Ensure the URL is using HTTP for local development
            if url and (url.startswith('https://127.0.0.1') or url.startswith('https://localhost')):
                url = url.replace('https://', 'http://')
            
            # Navigate to the URL
            if url:
                driver.get(url)
        
        # Wait for the page to load using explicit wait
        try:
            # Wait for common elements that indicate the page is loaded
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            print(f"Warning: Wait timed out: {e}")
        
        # Additional fixed wait to ensure page is fully rendered
        time.sleep(delay)
        
        # Run JavaScript to ensure content is visible and rendered
        try:
            # Force display of all elements
            driver.execute_script("""
                function forceShow(el) {
                    if (el.style) {
                        el.style.display = '';
                        el.style.visibility = 'visible';
                        el.style.opacity = 1;
                    }
                    if (el.childNodes && el.childNodes.length > 0) {
                        for (var i = 0; i < el.childNodes.length; i++) {
                            forceShow(el.childNodes[i]);
                        }
                    }
                }
                forceShow(document.body);
            """)
        except Exception as render_error:
            print(f"Warning: Error while ensuring content is visible: {render_error}")
        
        # Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"summary_screenshot_{timestamp}.png"
        
        # Full path to save the screenshot
        output_path = os.path.join(screenshots_dir, output_filename)
        
        # Get page dimensions and set window size using JavaScript
        total_height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        total_width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
            "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
            "document.documentElement.offsetWidth);"
        )
        
        # Set window size to capture the full page
        driver.set_window_size(total_width, total_height)
        
        # Additional wait after resizing
        time.sleep(1)
        
        # Take screenshot of the body element for better full page capture
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.screenshot(output_path)
        except Exception as e:
            print(f"Warning: Couldn't take body screenshot, falling back to full page: {e}")
            driver.save_screenshot(output_path)
        
        # Close the driver
        driver.quit()
        driver = None
        
        # Clean up temporary file if it exists
        if temp_html_file and os.path.exists(temp_html_file):
            try:
                os.remove(temp_html_file)
            except Exception as cleanup_error:
                print(f"Warning: Could not remove temporary HTML file: {cleanup_error}")
        
        return {
            'success': True,
            'path': output_path,
            'filename': os.path.basename(output_path)
        }
    
    except Exception as e:
        error_msg = f"Error taking screenshot: {str(e)}"
        print(error_msg)
        
        # Create an error screenshot
        error_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_filename = f"error_screenshot_{error_timestamp}.png"
        
        # Create a simple HTML error page
        if driver:
            try:
                # Create a simple HTML error page
                error_html = f"""
                <html>
                <head>
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif;
                            margin: 40px;
                            background-color: #f8f8f8;
                        }}
                        .error-container {{
                            border: 1px solid #e74c3c;
                            padding: 20px;
                            border-radius: 5px;
                            background-color: #fff;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        h2 {{ 
                            color: #e74c3c;
                            margin-top: 0;
                        }}
                        pre {{
                            background-color: #f1f1f1;
                            padding: 10px;
                            border-radius: 4px;
                            overflow-x: auto;
                        }}
                    </style>
                </head>
                <body>
                    <div class="error-container">
                        <h2>Screenshot Error</h2>
                        <p>An error occurred while trying to take the screenshot:</p>
                        <pre>{error_msg}</pre>
                    </div>
                </body>
                </html>
                """
                driver.execute_script(f"document.body.innerHTML = `{error_html}`;")
                
                # Get base directory and create screenshots directory
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                screenshots_dir = os.path.join(base_dir, 'static', 'screenshots')
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Save error screenshot
                error_path = os.path.join(screenshots_dir, error_filename)
                driver.save_screenshot(error_path)
                driver.quit()
                
                # Clean up temporary file if it exists
                if temp_html_file and os.path.exists(temp_html_file):
                    try:
                        os.remove(temp_html_file)
                    except:
                        pass
                
                return {
                    'success': False,
                    'error': error_msg,
                    'path': error_path,
                    'filename': error_filename
                }
            except Exception as error_screenshot_error:
                print(f"Error creating error screenshot: {error_screenshot_error}")
                # Continue to fallback return
        
        # Always close the driver if it exists
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        # Clean up temporary file if it exists
        if temp_html_file and os.path.exists(temp_html_file):
            try:
                os.remove(temp_html_file)
            except:
                pass
        
        return {
            'success': False,
            'error': error_msg
        } 