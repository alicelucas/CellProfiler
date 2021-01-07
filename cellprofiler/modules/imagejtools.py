from cellprofiler_core.module import Module
from cellprofiler_core.setting.subscriber import ImageSubscriber
import imagej
from multiprocessing import Process


class ImageJTools(Module):
    module_name = "ImageJTools"
    variable_revision_number = 1
    category = "Advanced"

    def create_settings(self):

        self.image_name = ImageSubscriber(
            text="Select the input image",
            value="None",
            doc="Choose the image to be cropped.",
        )

    def settings(self):
        return [self.image_name]

    def visible_settings(self):
        return [self.image_name]

    def do_work(self):
        ij = imagej.init()

    def run(self, workspace):
        p = Process(target=self.do_work)
        p.start()
        p.join()



